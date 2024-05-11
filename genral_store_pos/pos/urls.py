from django.urls import path
from .views import *
urlpatterns = [
    path('', addInvoice , name="addInvoice"),
    path('get_invoice', getInvoice , name="getInvoice")
]
