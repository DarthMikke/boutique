from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import View
from .rest_additions import TemplateListView, TemplateView
from django.http import HttpResponse

from .models import Receipt

# Create your views here.


class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponse(status=301, headers={
                "location": reverse('dashboard')
            })
        else:
            return HttpResponse(status=401)


class Dashboard(TemplateListView):
    template_name = "boutique/dashboard.html"
    model = Receipt
    identifiers = []


class ReceiptView(TemplateView):
    template_name = "boutique/receipt.html"
    model = Receipt
    identifiers = [('id', 'receipt_id')]
