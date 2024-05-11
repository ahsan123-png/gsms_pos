from .models import Invoice
from .serializers import *
from users.models import UserData
from users.views import good_response, bad_response, get_request_body
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
from django.db import transaction
from django.db.models import F
# ============ views ===============
@csrf_exempt
def addInvoice(request):
    if request.method == "POST":
        data = get_request_body(request)
        product_data = data.get('products', [])
        employee_user_id = data.get('employeeId', None)
        if employee_user_id is None:
            return JsonResponse(
                bad_response(
                    request.method,
                    {'error': 'User ID is required.'},
                    status=400
                )
            )
        try:
            employee = UserData.objects.get(id=employee_user_id)
        except UserData.DoesNotExist:
            return JsonResponse(
                bad_response(
                    request.method,
                    {'error': f'User with ID {employee_user_id} not found.'},
                    status=404
                )
            )

        invoice_number = generate_unique_invoice_number()
        total_amount = 0
        products_list = []
        
        try:
            with transaction.atomic():
                for product_item in product_data:
                    product_id = product_item.get('product_id', None)
                    qty = product_item.get('qty', 0)
                    unit = product_item.get('unit', '')  # Ensure 'unit' is properly set
                    if product_id is None or qty <= 0 or unit == '':
                        continue  # Skip invalid entries

                    product = AddProduct.objects.get(id=product_id)
                    if product.qtyPerPiece == 0:
                        return JsonResponse(
                            bad_response(
                                request.method,
                                {'error': f'Product "{product.productName}" is out of stock.'},
                                status=400
                            )
                        )
                    # Validate quantity
                    if product.qtyPerPiece < qty:
                        return JsonResponse(
                            bad_response(
                                request.method,
                                {'error': f'Insufficient quantity for product: {product.productName}'},
                                status=400
                            )
                        )

                    total_per_product = product.salePricePerPiece * qty
                    total_amount += total_per_product

                    # Update inventory quantity
                    product.qtyPerPiece = F('qtyPerPiece') - qty
                    product.save()

                    product_entry = {
                        'product_name': product.description,
                        'unit Price': product.salePricePerPiece,
                        'quantity': qty,
                        'total_per_product': total_per_product,
                        'unit': unit,  # Include 'unit' in product entry
                    }
                    products_list.append(product_entry)

                    Invoice.objects.create(
                        product_name=product.productName,
                        total_amount=product.salePricePerPiece,
                        quantity=qty,
                        unit=unit,
                        net_total=total_per_product,
                        product=product,
                        invoice_number=invoice_number,
                        employee_name=employee.name,
                    )
        except Exception as e:
            return JsonResponse(
                bad_response(
                    request.method,
                    f'Internal server error: {e}',
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

# ========= search and get the invoice ==========
@csrf_exempt
def getInvoice(request):
    if request.method == "POST":
        data=get_request_body(request)
        try:
            invoiceID=data.get('invoice_no','')
            if invoiceID is None:
                return JsonResponse(
                    bad_response(
                        request.method,
                        f'Not found invoice : {invoiceID}'
                    )
                )
            invoiceData = Invoice.objects.filter(invoice_number=invoiceID)

            if invoiceData is None:
                return JsonResponse(
                    bad_response(
                        request.method,
                        f"No record found against invoice id {invoiceID}",status=404

                    )
                )
            else:
                serializeData=InvoiceSerializer(invoiceData,many=True).data
                return JsonResponse(
                    good_response(
                        request.method,{
                            "invoice":serializeData
                        },status=200
                    )
                )
        except Exception as e:
            return JsonResponse(bad_response(
                request.method,
                f'Internal server error : {e}',status=500
            ))
    else:
        return JsonResponse(
            bad_response(
                request.method,
                f"{request.method} not allowed",
                status=405
            )
        )
def generate_unique_invoice_number():
    # Generate a random invoice number and check if it exists in the database
    while True:
        invoice_number = random.randint(5000000, 9999999)
        if not Invoice.objects.filter(invoice_number=invoice_number).exists():
            return invoice_number