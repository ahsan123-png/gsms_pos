from .models import *
from .serializers import *
from users.views import good_response,bad_response,get_request_body
from django.http.response import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import random
from inventory.models import AddProduct 
#============================

@csrf_exempt
def addInvoice(request):
    if request.method == "POST":
        data = get_request_body(request)
        productId = data.get('product_id', None)
        qty = data.get('qty', None)
        invoiceNumber=random.randint(500000,999999)
        if productId is None or qty is None:
            return JsonResponse(
                bad_response(
                    request.method,
                    "Product ID and quantity are required fields.",
                    status=400
                )
            )

        try:
            product = AddProduct.objects.get(id=productId)
        except AddProduct.DoesNotExist:
            return JsonResponse(
                bad_response(
                    request.method,
                    "Product does not exist.",
                    status=404
                )
            )

        invoice_data = Invoice.objects.create(
            product_name=product.productName,
            total_amount=product.salePricePerPiece,
            quantity=qty,
            net_total=product.salePricePerPiece * qty,
            product=product , # Assign the product object to the invoice
            invoice_number=invoiceNumber

        )
        invoice_data.save()

        return JsonResponse(
            good_response(
                request.method,
                "Invoice created successfully."
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

        
