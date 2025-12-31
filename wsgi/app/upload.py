from django.db import models
from django.forms import ModelForm
from django.http import HttpResponse
from django.urls import reverse

from app.rest_additions import TemplateView

import json


class Upload(models.Model):
    date = models.DateTimeField(
        name='date', db_column='date',
        null=True, blank=True,
    )
    provider = models.CharField(max_length=250)
    attachment = models.FileField(null=True, blank=True)
    raw = models.FileField(null=True, blank=True)


class ReceiptScanner:
    name: str = None
    """
    Name of the interpreter, will be used to fill in the result's
    provider.
    """

    def scan(self, upload: Upload) -> dict:
        """
        actual implementation goes here.
        """
        pass


class Service:
    # TODO: Make this a list of scanners and interpreters
    scanner: ReceiptScanner = None
    receipt_import_service = None

    import_path_name = 'upload_process'

    def __init__(self, scanner: ReceiptScanner):
        self.scanner = scanner

    def interpret_upload(self, upload: Upload):
        raw_interpretation = self.scanner.scan(upload)
        upload.raw = json.dumps(raw_interpretation)
        upload.provider = self.scanner.name

        upload.save()


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

        self.service.interpret_upload(upload)

        return HttpResponse(status=302, headers={
            "location": reverse(self.service.import_path_name,
                                kwargs={'upload_id': upload.id})
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReceiptUploadForm()
        return context
