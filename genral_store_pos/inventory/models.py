from django.db import models

class AddSupplier(models.Model):
    name = models.CharField(max_length=50)
    phoneNumber = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class AddProduct(models.Model):
    companyName = models.CharField(max_length=50)
    productName = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    purchasePricePerPiece = models.DecimalField(max_digits=10, decimal_places=2)
    purchasePricePerCotton = models.DecimalField(max_digits=10, decimal_places=2)
    salePricePerPiece = models.DecimalField(max_digits=10, decimal_places=2)
    salePricePerCotton = models.DecimalField(max_digits=10, decimal_places=2)
    qtyPerCotton = models.PositiveIntegerField()
    qtyPerPiece = models.PositiveIntegerField()
    piecesInCotton = models.PositiveIntegerField()  # New field
    supplier = models.ForeignKey(AddSupplier, on_delete=models.CASCADE)

    def __str__(self):
        return self.productName
