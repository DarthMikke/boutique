from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import View
from .rest_additions import TemplateListView, TemplateView
from django.http import HttpResponse

from .models import Receipt
from .forms import ReceiptForm, PurchaseFormSet

# Create your views here.


class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponse(status=302, headers={
                "location": reverse('dashboard')
            })
        else:
            return HttpResponse(status=302, headers={
                "location": '/admin'
            })


class Dashboard(TemplateListView):
    template_name = "boutique/dashboard.html"
    model = Receipt
    identifiers = []


class ReceiptView(TemplateView):
    template_name = "boutique/receipt.html"
    model = Receipt
    identifiers = [('id', 'receipt_id')]


class ReceiptNewView(TemplateView):
    template_name = "boutique/receipt_edit.html"
    identifiers = []

    def post(self, request):
        form = ReceiptForm(request.POST)
        return HttpResponse(repr(form), content_type='text/plain')

        if form.is_valid():
            form.save()
            return HttpResponse(status=302, headers={
                "location": reverse('dashboard')
            })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReceiptForm()
        context['formset'] = PurchaseFormSet(initial=[{'quantity': 1}])
        print(repr(context['formset']))
        print(repr(context['formset'].management_form))
        return context


class ReceiptUploadView(TemplateView):
    template_name = "boutique/receipt_upload.html"
    identifiers = []

    def post(self, request):
        form = ReceiptForm(request.POST)
        return HttpResponse(repr(form), content_type='text/plain')

        if form.is_valid():
            form.save()
            # Start analyzing
            return HttpResponse(status=302, headers={
                "location": reverse('dashboard')
            })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReceiptForm()
        return context
