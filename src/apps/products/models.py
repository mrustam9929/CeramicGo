from django.db import models
from django.db.models import Sum, Q

from apps.users.models import User


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'products'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    @property
    def count(self) -> int:
        products = ProductInventoryOperation.objects.filter(product=self).aggregate(
            receipt=Sum('count', filter=Q(operation_type=ProductInventoryOperation.OperationType.RECEIPT), default=0),
            sale=Sum('count', filter=Q(operation_type=ProductInventoryOperation.OperationType.SALE), default=0),
            defect=Sum('count', filter=Q(operation_type=ProductInventoryOperation.OperationType.DEFECT), default=0),
        )
        return products['receipt'] - products['sale'] - products['defect']


class ProductInventoryOperation(models.Model):
    class OperationType(models.TextChoices):
        RECEIPT = 'receipt', 'Поступление'
        SALE = 'sale', 'Продажа'
        DEFECT = 'defect', 'Брак'

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='inventory_operations')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory_operations')
    count = models.SmallIntegerField(default=0)
    operation_type = models.CharField(max_length=50, choices=OperationType.choices, db_index=True)
    price = models.DecimalField(decimal_places=0, max_digits=10)

    class Meta:
        db_table = 'product_entry_exit'
        verbose_name = 'Учет товара'
        verbose_name_plural = 'Учет товаров'
