from django.db import models
from inventory.models import AddProduct  # Assuming AddProduct is the model for product data

class Invoice(models.Model):
    date = models.DateField(auto_now_add=True)
    invoice_number = models.IntegerField()
    product = models.ForeignKey(AddProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    net_total = models.DecimalField(max_digits=10, decimal_places=2)
    product_name = models.CharField(max_length=50)
    employee_name = models.CharField(max_length=50,default='unknown')
    unit = models.CharField(max_length=50,default='unknown')
    

    def __str__(self):
        return f"Invoice {self.invoice_number}"

    def save(self, *args, **kwargs):
        # Calculate net total based on quantity and product price
        self.net_total = self.quantity * self.product.salePricePerPiece
        super().save(*args, **kwargs)



    def __str__(self):
        return self.productName
