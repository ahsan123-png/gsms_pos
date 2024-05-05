from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [

    path('add_supplier',supplier,name="supplier"),
    path('add_product',addProduct,name="addProduct"),
    path('view_inventory',viewInventory,name="viewInventory"),
]
