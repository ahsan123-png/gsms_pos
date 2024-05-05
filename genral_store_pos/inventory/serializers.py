from .models import *
from rest_framework import serializers
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddProduct
        fields = "__all__"
        