import os

from django.urls import path
from .views import *

from .imported_receipt import Service
from .azure import *

azure_endpoint = os.environ['AZURE_ENDPOINT']
azure_key = os.environ['AZURE_KEY']
ReceiptUploadView.service = Service(
     AzureReceiptScanner(azure_endpoint, azure_key),
     AzureReceiptInterpreter()
)

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
    # path('imports/<import_id>/process', ImportProcessView.as_view(),
    #      name='import_process')
    path('receipts/new', ReceiptNewView.as_view(), name='receipt_new'),
    path('receipts/upload', ReceiptUploadView.as_view(),
         name='receipt_upload'),
    path('receipts/<receipt_id>', ReceiptView.as_view(), name='receipt'),
    path('receipts/analyze/<receipt_id>', ReceiptAnalyzeView.as_view(),
         name='receipt_analyze'),
    # path('accounts', BankAccountList, name='bank_account_list'),
    # path('accounts/add', BankAccountAdd, name='bank_add'),
    # path('accounts/<account_id>', BankAccount, name='bank_account'),
]
