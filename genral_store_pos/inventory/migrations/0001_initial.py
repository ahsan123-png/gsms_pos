# Generated by Django 5.0.4 on 2024-05-02 11:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AddSupplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phoneNumber', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='AddProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyName', models.CharField(max_length=50)),
                ('productName', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=255)),
                ('purchasePricePerPiece', models.DecimalField(decimal_places=2, max_digits=10)),
                ('purchasePricePerCotton', models.DecimalField(decimal_places=2, max_digits=10)),
                ('salePricePerPiece', models.DecimalField(decimal_places=2, max_digits=10)),
                ('salePricePerCotton', models.DecimalField(decimal_places=2, max_digits=10)),
                ('qtyPerCotton', models.PositiveIntegerField()),
                ('qtyPerPiece', models.PositiveIntegerField()),
                ('piecesInCotton', models.PositiveIntegerField()),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.addsupplier')),
            ],
        ),
    ]
