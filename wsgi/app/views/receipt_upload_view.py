from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.core.files.base import ContentFile

from app.rest_additions import TemplateView
from app.models import Receipt
from app.forms import ReceiptScanUploadForm

import os

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
import json
import uuid


class ReceiptUploadView(TemplateView):
    template_name = "boutique/receipt_upload.html"
    identifiers = []

    def post(self, request):
        form = ReceiptScanUploadForm(request.POST, request.FILES)
        valid = form.is_valid()

        if not valid:
            # TODO nice error message
            return HttpResponse(repr(form), status=500,
                                content_type='text/plain')

        receipt: Receipt = form.save()

        endpoint = os.environ['AZURE_ENDPOINT']
        credential = AzureKeyCredential(os.environ['AZURE_KEY'])

        # Start analyzing
        document_intelligence_client = DocumentIntelligenceClient(
            endpoint, credential
        )
        with open(receipt.picture.path, 'rb') as f:
            print("Started analyzing")
            poller = document_intelligence_client.begin_analyze_document(
                "prebuilt-receipt", body=f, locale="no-NO"
            )
            analyzed_path = str(uuid.uuid4()) + '.json'
            receipts: AnalyzeResult = poller.result()

        receipt.analyzed.save(
            analyzed_path,
            ContentFile(json.dumps(receipts.as_dict()))
        )
        receipt.save()

        receipt.analyze()

        return HttpResponse(status=302, headers={
            "location": reverse('dashboard')
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReceiptScanUploadForm()
        return context
