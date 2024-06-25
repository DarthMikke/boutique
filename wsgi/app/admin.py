from django.contrib import admin
from .models import *


class PurchaseInline(admin.TabularInline):
    model = Purchase


class ReceiptAdmin(admin.ModelAdmin):
    list_display = ['date', 'store', 'total_amount']
    fieldsets = [
        (
            None,
            {
                "fields": ['store', 'date', ]
            }
        )
    ]
    inlines = [
        PurchaseInline,
    ]


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand']


# Register your models here.
admin.site.register(Store)
admin.site.register(Brand)
admin.site.register(Product, ProductAdmin)
admin.site.register(Receipt, ReceiptAdmin)
