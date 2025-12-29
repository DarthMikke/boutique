from django.contrib import admin
from .models import *
import app.upload
import app.imported_receipt


class PurchaseInline(admin.TabularInline):
    model = Purchase


class ReceiptAdmin(admin.ModelAdmin):
    list_display = ['date_admin', 'store', 'total_amount']
    fieldsets = [
        ( None, {
            "fields": ['picture', ],
        }),
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


class ImportedLineItemInline(admin.TabularInline):
    model = app.imported_receipt.ImportedLineItemModel


class ImportedReceiptAdmin(admin.ModelAdmin):
    inlines = [
        ImportedLineItemInline,
    ]


# Register your models here.
admin.site.register(app.upload.Interpretation)
admin.site.register(app.imported_receipt.ImportedReceipt, ImportedReceiptAdmin)
admin.site.register(app.imported_receipt.ImportedLineItemModel)
admin.site.register(Store)
admin.site.register(Brand)
# admin.site.register(ProductSize)
admin.site.register(Product, ProductAdmin)
admin.site.register(Receipt, ReceiptAdmin)
# admin.site.register(AnalyzedStoreAlias)
