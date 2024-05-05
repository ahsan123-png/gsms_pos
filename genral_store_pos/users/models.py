from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserData(User):
    name = models.CharField(max_length=50)
    phoneNumber = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    designation = models.CharField(max_length=120)
    employeeIdNo = models.IntegerField()

    def __str__(self):
        return self.name
