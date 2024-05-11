
from .models import *
from rest_framework import serializers
class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = [
            'id',
            'date',
            'invoice_number',
            'product',
            'quantity',
            'total_amount',
            'net_total',
            'product_name',
            'employee_name',
            'unit',
        ]
        