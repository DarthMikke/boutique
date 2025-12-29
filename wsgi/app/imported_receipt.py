from django.db import models
from django.forms import ModelForm
from django.http import HttpResponse
from django.urls import reverse

from app.rest_additions import TemplateView
from app.upload import ReceiptScanner, Upload

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
    scanner: ReceiptScanner = None
    interpreter: Interpreter = None
    receipt_service = None

    def __init__(
        self,
        scanner: ReceiptScanner,
        interpreter: Interpreter,
        receipt_service=None,
    ):
        self.scanner = scanner
        self.interpreter = interpreter
        self.receipt_service = receipt_service

    def create_receipts_from_interpretation(self,
                                            upload: Upload):
        raw_interpretation = self.scanner.scan(upload)
        upload.raw = json.dumps(raw_interpretation)
        upload.provider = self.scanner.name

        upload.save()

        imported_receipts = self.interpreter.interpret(raw_interpretation)
        if self.receipt_service:
            for r in imported_receipts:
                receipt = self.receipt_service.from_imported(r)
                receipt.save()


class ReceiptUploadForm(ModelForm):
    class Meta:
        model = Upload
        fields = [
            'attachment',
        ]


class ReceiptUploadView(TemplateView):
    template_name = "boutique/receipt_upload.html"
    identifiers = []
    service: Service = None

    def post(self, request):
        form = ReceiptUploadForm(request.POST, request.FILES)
        valid = form.is_valid()

        if not valid:
            # TODO nice error message
            return HttpResponse(repr(form), status=500,
                                content_type='text/plain')

        upload: interpretation.Model = form.save()
        upload.save()

        self.service.create_receipts_from_interpretation(upload)

        return HttpResponse(status=302, headers={
            "location": reverse('dashboard')
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReceiptUploadForm()
        return context
