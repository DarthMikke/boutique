from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import View, TemplateView
from django.views.generic.list import ListView
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


class Dashboard(ListView):
    template_name = "boutique/dashboard.html"
    model = Receipt
