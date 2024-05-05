from django.http import JsonResponse
from django.shortcuts import render
from .models import *
from .serializers import *
from users.views import good_response,bad_response,get_request_body,check_required_fields,clean_phone_number
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@csrf_exempt
def supplier(request):
    if request.method == "POST":
        try:    
            required_felids=['name',"phone"]
            data=get_request_body(request)
            name=data.get('name')
            phoneNumber=data.get('phone')
            check_required_fields(data,required_felids)
            if AddSupplier.objects.filter(name=name):
               return JsonResponse(bad_response(
                  request.method,
                  f"Company Already registered with name {name}"
               ))
            sup=AddSupplier.objects.create(name=name,phoneNumber=phoneNumber)
            sup.save()
            return JsonResponse(good_response(
                                request.method,
                                {"success" : "Data Added successfully"}
                          
                          )
            )
        except Exception as e:
           return JsonResponse(bad_response(request.method,
              f'internal system error : {e}' , status=500
           ))
    else:
     return JsonResponse(bad_response(request.method, 
                                         f"{request.method} not allowed", 
                                         status=405))   
@csrf_exempt
def addProduct(request):
    if request.method == "POST":
        try:
            req_dict = get_request_body(request)
            required_fields = [
                'companyName',
                'productName',
                'description',
                'purchasePricePerPiece',
                'purchasePricePerCotton',
                'salePricePerPiece',
                'salePricePerCotton',
                'qtyPerCotton',
                'qtyPerPiece',
                'piecesInCotton',
                'supplier'
            ]
            check_required_fields(req_dict, required_fields)
            # Retrieve supplier ID from request data
            supplier_id = req_dict.get('supplier')
            # Check if the supplier ID exists in the AddSupplier model
            if not AddSupplier.objects.filter(id=supplier_id).exists():
                return JsonResponse(
                    bad_response(
                        request.method,
                        {"error": f"Supplier with ID {supplier_id} does not exist"},
                        status=404
                    )
                )
            # Create the AddProduct instance with the validated supplier ID
            invData = AddProduct.objects.create(
                companyName=req_dict.get('companyName', ''),
                productName=req_dict.get('productName', ''),
                description=req_dict.get('description', ''),
                purchasePricePerPiece=req_dict.get('purchasePricePerPiece', ''),
                purchasePricePerCotton=req_dict.get('purchasePricePerCotton', ''),
                salePricePerPiece=req_dict.get('salePricePerPiece', ''),
                salePricePerCotton=req_dict.get('salePricePerCotton', ''),
                qtyPerCotton=req_dict.get('qtyPerCotton', ''),
                qtyPerPiece=req_dict.get('qtyPerPiece', ''),
                piecesInCotton=req_dict.get('piecesInCotton', ''),
                supplier_id=supplier_id  # Associate with the validated supplier ID
            )
            invData.save()
            return JsonResponse(
                good_response(
                    request.method,
                    {"success": "Data Added successfully"}
                )
            )
        except Exception as e:
            return JsonResponse(
                bad_response(
                    request.method,
                    f'Internal system error: {e}',
                    status=500
                )
            )
    else:
        return JsonResponse(
            bad_response(
                request.method,
                f"{request.method} not allowed",
                status=405
            )
        )

       


