from django.contrib.auth.hashers import check_password 
from django.contrib.auth import authenticate,login,logout
from typing import Any
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .serializers import *
from .models import *
import random

# Create your views here.
@csrf_exempt
def addEmployee(request):
    if request.method == "POST":
        try:
            required_fields = ['first_name',
                                'last_name',
                                'email',
                                'password',
                                'designation',
                                'gender',
                                'phoneNumber']
            employee_data = get_request_body(request)
            check_required_fields(employee_data, required_fields) 
            employee_id = random.randint(100000, 999999)
            first_name = employee_data.get('first_name', '')
            last_name = employee_data.get('last_name', '')
            password = employee_data.get('password', '')
            designation = employee_data.get('designation', '')
            gender = employee_data.get('gender', '')
            phone_number = employee_data.get('phoneNumber', '')
            email = employee_data.get('email', '')
            name = f"{first_name} {last_name}"
            username = email.split("@")[0]
            emp_data = UserData.objects.create(
                name=name,
                password=password,
                employeeIdNo=employee_id,
                gender=gender,
                designation=designation,
                phoneNumber=phone_number,
                username=username,
                email=email
            )
            emp_data.save()
            context={
                'name' :name,
                'employee_id' :employee_id,
                'designation': designation,

            }
            return JsonResponse(good_response
                                (request.method,
                                {"success": "Data added successfully",
                                 "data" : context}))
        except Exception as e:
            return JsonResponse(bad_response
                                (request.method, str(e),
                                  status=400))
    else:
        return JsonResponse(bad_response(request.method, 
                                         f"{request.method} not allowed", 
                                         status=405))
# ======= Login User =============
@csrf_exempt
def empLogin(request):
    if request.method == 'POST':
        try:
            req_dict=get_request_body(request)
            empId=req_dict.get("employeeId")
            empPassword=req_dict.get('empPassword')
            if empId is None or empPassword is None:
                return JsonResponse(
                bad_response(
                    request.method,
                    {"error": "Employee/Password is required "},
                    status=404
                )
            )
        # check the user with employee id exits in database or not 
            user=UserData.objects.get(employeeIdNo=empId)
            if user is None:
                return JsonResponse(
                bad_response(
                    request.method,
                    {"error": f"User with id {empId} does not exist in the database"},
                    status=404
                )
            )
            # check if the password not match
            userData=check_password(empPassword, user.password)
            if userData is None:
                return JsonResponse(
                    bad_response(
                        request.method,
                        {"error": "Invalid password"},
                        status=401
                    )
                )
            # User and password are correct, return success response
            return JsonResponse(
                good_response(
                    request.method,
                    {"success": "Login successful"}
                )
            )
        except UserData.DoesNotExist:
            return JsonResponse(
                bad_response(
                    request.method,
                    {"error": "User does not exist in the database"},
                    status=404
                )
            )
    else:
        return JsonResponse(bad_response(request.method, 
                                         f"{request.method} not allowed", 
                                         status=405))
#=========== View all employees ===========
def allEmployees(request):
    if request.method == "GET":
        # import pdb;pdb.set_trace()
        user_data=[]
        user=UserData.objects.all()
        if user is None:
            return JsonResponse(bad_response(
                request.method,{
                    'error' : "No Employee Data Find"
                },status=404
            ))
        for users in user:
            serialize= EmplyeeSerializer(users).data
            user_data.append(serialize)
        return JsonResponse(
            good_response(
                request.method,
                {"success":"Display Employee all data",
                 'data' :user_data},status=200
            )
        )
    else:
        return JsonResponse(
            bad_response(
                request.method,
                {"error" : f'Method {request.method} Not Allowed'}
            )
        )
#get by id 
def getEmployeeById(request,id):
    if request.method== 'GET':
        try:
            user=UserData.objects.get(id=id)
            serialize= EmplyeeSerializer(user).data
            return JsonResponse(good_response(
                request.method,
                {
                    'user_data' : serialize
                }
            ))
        except UserData.DoesNotExist:
            return JsonResponse(
                bad_response(
                    request.method,
                    {"error": "User does not exist in the database"},
                    status=404
                )
            )
        except Exception as e:
            return JsonResponse(bad_response("POST", f'unexpected error occur : {e}', status=400))
    else:
        return JsonResponse(
            bad_response(
                request.method,
                {"error" : f'Method {request.method} Not Allowed'}
            )
        )
# delete by id
@csrf_exempt
def deleteEmplyeeById(request,id):
    if request.method== 'DELETE':
        try:
            user=UserData.objects.get(id=id)
            user.delete()
            return JsonResponse(good_response(
                request.method,
                {
                    'Message' : f"user with id {id} delete successfully"
                },status=200
            ))
        except UserData.DoesNotExist:
            return JsonResponse(
                bad_response(
                    request.method,
                    {"error": "User does not exist in the database"},
                    status=404
                )
            )
        except Exception as e:
            return JsonResponse(bad_response("POST", f'unexpected error occur : {e}', status=400))
    else:
        return JsonResponse(
            bad_response(
                request.method,
                {"error" : f'Method {request.method} Not Allowed'}
            )
        )
# update by id
@csrf_exempt
def updateEmployeeById(request,id):
    if request.method == 'PUT':
        try:     
            user=UserData.objects.get(id=id)
            req_dict= get_request_body(request)
            old_data=EmplyeeSerializer(user, context={'request': request}).data
            if "name" in req_dict:
                user.name=req_dict['name']
            if "email" in req_dict:
                user.email=req_dict['email']
            if "phone_number" in req_dict:
                user.phoneNumber=req_dict['phone_number']
            new_data=EmplyeeSerializer(user, context={'request': request}).data
            return JsonResponse(
                good_response(
                    request.method,
                    {
                        "old_data" : old_data,
                        'new_data' : new_data
                    }
                )
            )
        except UserData.DoesNotExist:
            return JsonResponse(
                bad_response(
                    request.method,
                    {"error": "User does not exist in the database"},
                    status=404
                )
            )

    else:
        return JsonResponse(
            bad_response(
                request.method,
                {"error" : f'Method {request.method} Not Allowed'}
            )
        )
#========= when we require specific felids in response ==========
"""    users = UserData.objects.all()
    users_data = []
    for user in users:
        user_info = {
            "name": user.name,
            "username": user.username,
            "email": user.email,
        }
        users_data.append(user_info)
    return JsonResponse({"users": users_data})"""
    
    


#========= missing value check function =============
def check_required_fields(data, required_fields):
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        error_message = f"Required fields missing: {', '.join(missing_fields)}"
        raise ValueError(error_message)
    
# useful functions 
def get_request_body(request):
    return json.loads(request.body)


def good_response(method: str, data: dict | Any, status: int = 200):
    return {
        "success": True,
        "data": data,
        "method": method,
        "status": status,
    }


def bad_response(method: str, reason: str, status: int = 403, data: dict | Any = None):
    return {
        "success": False,
        "reason": reason,
        "data": data,
        "status": status,
        "method": method,
    }


def clean_phone_number(phone_number):
    if phone_number.__contains__("+"):
        phone_number = phone_number.replace("+", "")
    if phone_number.__contains__(" "):
        phone_number = phone_number.replace(" ", "")
    if phone_number.__contains__("-"):
        phone_number = phone_number.replace("-", "")
    return phone_number
