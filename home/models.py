from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    birthday = models.DateField(blank=True, null=True)
    frequency = models.PositiveIntegerField(default=30, help_text="Días entre visitas sugeridas")
    notes = models.TextField(blank=True)
    last_visit = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    min_stock = models.PositiveIntegerField(default=0)
    for_sale = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.product_name


class Transaction(models.Model):
    SERVICE = 'service'
    SALE = 'sale'
    PURCHASE = 'purchase'

    TRANSACTION_CHOICES = [
        (SERVICE, 'Servicio'),
        (SALE, 'Venta'),
        (PURCHASE, 'Compra'),
    ]

    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_CHOICES)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    items = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.get_transaction_type_display()} - {self.description}"
