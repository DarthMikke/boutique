import os

from django.urls import path
from .views import *

import app.upload
import app.imported_receipt
from .azure import *

azure_endpoint = os.environ['AZURE_ENDPOINT']
azure_key = os.environ['AZURE_KEY']

upload_service = app.upload.Service(
    AzureReceiptScanner(azure_endpoint, azure_key),
)

receipt_import_service = app.imported_receipt.Service(
    AzureReceiptInterpreter(),
)

app.upload.ReceiptUploadView.service = upload_service
app.imported_receipt.UploadProcessView.service = receipt_import_service

urlpatterns = [
    path('', Login.as_view(), name='login'),
    path('dash', Dashboard.as_view(), name='dashboard'),
    # path('stores', StoreList, name='store_list'),
    # path('stores/add', StoreView, name='store_add'),
    # path('stores/<store_id>', StoreView, name='store'),
    # path('chains', ChainList, name='chain_list'),
    # path('chains/add', ChainView, name='chain_add'),
    # path('chains/<store_id>', ChainView, name='chain'),
    # path('products', GroceryGroupList, name='product_group_list'),
    # path('products/<group_id>', GroceryGroupView, name='product_group'),
    # path('products/add_group', GroceryGroupView, name='product_group_add'),
    # path('products/<group_id>/<product_id>', ProductView, name='product'),
    # path('products/add', ProductView, name='product_add'),
    # path('brands', BrandList, name='brand_list'),
    # path('brands/add', BrandView, name='brand_add'),
    # path('brands/<brand_id>', BrandView, name='brand'),
    # path('receipts', ReceiptList, name='receipt_list'),
    path('receipts/<upload_id>/process', app.imported_receipt.UploadProcessView
         .as_view(),
         name=upload_service.import_path_name),
    path('receipts/new', ReceiptNewView.as_view(), name='receipt_new'),
    path('receipts/upload', app.upload.ReceiptUploadView.as_view(),
         name='receipt_upload'),
    path('receipts/<receipt_id>', ReceiptView.as_view(), name='receipt'),
    path('receipts/analyze/<receipt_id>', ReceiptAnalyzeView.as_view(),
         name='receipt_analyze'),
    # path('accounts', BankAccountList, name='bank_account_list'),
    # path('accounts/add', BankAccountAdd, name='bank_add'),
    # path('accounts/<account_id>', BankAccount, name='bank_account'),
]
