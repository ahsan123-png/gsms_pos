from .models import *
from rest_framework import serializers


class EmplyeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = [
            'id',
            'employeeIdNo',
            'password',
            'username',
            'email',
            'name',
            'date_joined',
            'phoneNumber',
            'gender',
            'designation',
        ]