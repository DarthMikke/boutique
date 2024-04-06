from django.urls import path
from .views import *

urlpatterns = [
    path('', Login.as_view(), name='login'),
    path('dash', Dashboard.as_view(), name='dashboard'),
    # path('stores', StoreList, name='store_list'),
    # path('stores/<store_id>', StoreView, name='store'),
    # path('groceries', GroceryGroupList, name='grocery_group_list'),
    # path('groceries/<group>', GroceryGroupView, name='grocery_group'),
    # path('groceries/<group>/<grocery>', GroceryView, name='grocery'),
    # path('brands', BrandList, name='brand_list'),
    # path('brands/<brand_id>', BrandView, name='brand'),
    # path('receipt', ReceiptList, name='receipt_list'),
    # path('receipt/<brand_id>', ReceiptView, name='receipt'),
]
