
from .models import *
from rest_framework import serializers
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = "__all__"
        