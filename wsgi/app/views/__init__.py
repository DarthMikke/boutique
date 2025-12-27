from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import View
from app.rest_additions import TemplateListView, TemplateView
from django.http import HttpResponse

from app.models import Receipt
from app.forms import ReceiptForm, PurchaseFormSet
from app.imported_receipt import ReceiptUploadView

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


class ReceiptAnalyzeView(TemplateView):
    template_name = "boutique/receipt.html"
    model = Receipt
    identifiers = [('id', 'receipt_id')]

    # TODO Should be POST, not GET
    def get(self, request, **kwargs):
        super().get(request, **kwargs)
        self.instance.analyze()

        return HttpResponse(status=302, headers={
            "location": reverse('receipt',
                                kwargs={'receipt_id': self.instance.id})
        })


class ReceiptNewView(TemplateView):
    template_name = "boutique/receipt_edit.html"
    identifiers = []

    def post(self, request):
        form = ReceiptForm(request.POST, request.FILES)
        # TODO A nice form
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
        return context
