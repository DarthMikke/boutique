from django.forms import ModelForm
from .models import Receipt

class ReceiptForm(ModelForm):
    class Meta:
        model = Receipt
        fields = [
            'picture',
            'date',
            'store',
            # 'purchases'
        ]
        # list_display = ['date', 'store', 'total_amount']
