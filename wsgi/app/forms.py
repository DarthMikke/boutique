from django.forms import ModelForm, inlineformset_factory
from .models import Receipt, Purchase


class ReceiptScanUploadForm(ModelForm):
    class Meta:
        model = Receipt
        fields = [
            'picture',
        ]


class ReceiptForm(ModelForm):
    class Meta:
        model = Receipt
        fields = [
            'picture',
            'date',
            'store',
        ]


PurchaseFormSet = inlineformset_factory(
    Receipt,
    Purchase,
    fields=[
        'product',
        'amount',
        'total_price',
        'discount'
    ],
    extra=1
)
