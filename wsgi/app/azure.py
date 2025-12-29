# Documentation available at:
# https://learn.microsoft.com/en-us/python/api/overview/azure/ai-documentintelligence-readme

from datetime import datetime

from django.core.files.base import ContentFile

import json
import uuid

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult

from app.upload import ReceiptScanner, Upload
from app.imported_receipt import Interpreter, ImportedReceipt, \
    ImportedLineItemModel


class AzureReceiptScanner(ReceiptScanner):
    name = 'azure'

    def __init__(self, endpoint, key):
        self.endpoint = endpoint
        self.credential = AzureKeyCredential(key)

        self.client = DocumentIntelligenceClient(
            self.endpoint, self.credential
        )

    def scan(self, upload: Upload) -> dict:
        with open(upload.attachment.path, 'rb') as f:
            print("Started analyzing")
            poller = self.client.begin_analyze_document(
                "prebuilt-receipt", body=f, locale="no-NO"
            )
            analyzed_path = str(uuid.uuid4()) + '.json'
            receipts: AnalyzeResult = poller.result()

        upload.raw.save(
            analyzed_path,
            ContentFile(json.dumps(receipts.as_dict()))
        )

        return receipts.as_dict()


class AzureReceiptInterpreter(Interpreter):
    name = 'azure'

    def interpret(self, data: dict) -> [ImportedReceipt]:
        print("Started interpreting documents")
        analyzed = AnalyzeResult(data)

        receipts: [ImportedReceipt] = []
        for doc in analyzed.documents:
            fields = doc.fields
            transaction_tstamp = (
                fields['TransactionDate']['valueDate'],
                fields['TransactionTime']['valueTime']
                if 'TransactionTime' in fields.keys()
                else '12:00:00'
            )
            transaction_dt = datetime.fromisoformat(
                "%s %s" % transaction_tstamp
            )

            price = float(fields['Total']['valueCurrency']['amount'])
            currency = fields['Total']['valueCurrency']['currencyCode']

            address = fields['MerchantAddress'].value_address \
                if 'MerchantAddress' in fields.keys() else None
            merchant_address = None
            if address is not None:
                merchant_address = ''

                street_address = address.street_address
                if street_address:
                    merchant_address += street_address + ', '

                postal_code = address.postal_code
                if postal_code is not None:
                    merchant_address += postal_code + ' '

                city = address.city
                if city is not None:
                    merchant_address += city

            merchant = fields['MerchantName'].value_string \
                if 'MerchantName' in fields.keys() else None

            r = ImportedReceipt(
                date=transaction_dt,
                merchant=merchant,
                merchantAddress=merchant_address,
                totalPrice=price,
                currency=currency,
                interpretation=None)
            r.save()
            receipts.append(r)

            for li in fields['Items'].value_array:
                fs = li.value_object
                product = fs['Description'].value_string \
                    if 'Description' in fs.keys() else None
                quantity = float(fs['Quantity'].value_number) \
                    if 'Quantity' in fs.keys() else None
                quantityUnit = fs['QuantityUnit'].value_string \
                    if 'QuantityUnit' in fs.keys() else None
                totalPrice = float(fs['TotalPrice'].value_currency.amount) \
                    if 'TotalPrice' in fs.keys() else None
                currency = fs['TotalPrice'].value_currency.currency_code \
                    if 'TotalPrice' in fs.keys() else None

                line_item = ImportedLineItemModel(
                    product=product,
                    quantity=quantity,
                    quantityUnit=quantityUnit,
                    totalPrice=totalPrice,
                    currency=currency,
                    parent=r,
                )
                line_item.save()

        return receipts
