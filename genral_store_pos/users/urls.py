from django.contrib import admin
from django.urls import path,include
from .views import *
urlpatterns = [

    path('add_users',addEmployee,name="addEmployee"),
    path('login_employee',empLogin,name="empLogin"),
    path('all',allEmployees,name="allEmployees"),
    path('get/<int:id>',getEmployeeById,name="getEmployeeById"),
    path('update/<int:id>',updateEmployeeById,name="updateEmployeeById"),
    path('delete/<int:id>',deleteEmplyeeById,name="deleteEmplyeeById"),
]
