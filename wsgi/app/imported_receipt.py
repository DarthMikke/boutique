from django.db import models
from django.forms import ModelForm
from django.http import HttpResponse, JsonResponse
from django.urls import reverse

from app.rest_additions import TemplateView
from app.upload import Upload

import json


class Interpreter:
    def interpret(self, data: str):
        pass


class ImportedReceipt(models.Model):
    date = models.DateTimeField(
        name='date', db_column='date',
        null=True, blank=True,
    )
    merchant = models.CharField(max_length=250,
                                null=True, blank=True)
    merchantAddress = models.CharField(max_length=250,
                                       null=True, blank=True)
    totalPrice = models.DecimalField(max_digits=7, decimal_places=2,
                                     null=True, blank=True)
    currency = models.CharField(max_length=10,
                                null=True, blank=True)
    interpretation = models.ForeignKey(Upload,
                                       on_delete=models.SET_NULL,
                                       null=True,
                                       blank=True,
                                       related_name='imported_receipts')


class ImportedLineItemModel(models.Model):
    product = models.CharField(max_length=250,
                               null=True, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=3,
                                   null=True, blank=True)
    quantityUnit = models.CharField(max_length=250,
                                    null=True, blank=True)
    totalPrice = models.DecimalField(max_digits=7, decimal_places=2,
                                     null=True, blank=True)
    currency = models.CharField(max_length=10,
                                null=True, blank=True)
    parent = models.ForeignKey(ImportedReceipt, on_delete=models.CASCADE,
                               related_name='line_items')


class Service:
    # TODO: Make this a list of scanners and interpreters
    interpreter: Interpreter = None
    receipt_service = None

    def __init__(
        self,
        interpreter: Interpreter,
        receipt_service=None,
    ):
        self.interpreter = interpreter
        self.receipt_service = receipt_service

    def create_import_from_upload(self, upload: Upload):
        # TODO: Maybe should check if the interpreter's name is the same
        # as scanner's?
        # upload.provider == self.interpreter.name

        imported_receipts = self.interpreter.interpret(upload)
        if self.receipt_service:
            for r in imported_receipts:
                receipt = self.receipt_service.from_imported(r)
                receipt.save()


class UploadProcessView(TemplateView):
    template_name = "boutique/upload_process.html"
    identifiers = [('id', 'upload_id')]
    model = Upload
    service: Service = None

    def get(self, request, **kwargs):
        self.service.create_import_from_upload(self.instance)

        return super().get(request, **kwargs)
