from decimal import Decimal
from platform import processor

from django.db import models
from django.db.models import Sum, Q

from apps.users.models import User


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')

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

    @property
    def price(self) -> Decimal:
        last_receipt = ProductInventoryOperation.objects.filter(
            product=self, operation_type=ProductInventoryOperation.OperationType.RECEIPT
        ).order_by('-created_at').first()
        if last_receipt is None:
            return Decimal('0')
        return last_receipt.price


class ProductInventoryOperation(models.Model):
    class OperationType(models.TextChoices):
        RECEIPT = 'receipt', 'Поступление'
        SALE = 'sale', 'Продажа'
        DEFECT = 'defect', 'Брак'

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='inventory_operations',
                             verbose_name='Сотрудник')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory_operations',
                                verbose_name='Продукт')
    count = models.SmallIntegerField(default=0, verbose_name='Кол-во')
    operation_type = models.CharField(max_length=50, choices=OperationType.choices, db_index=True, verbose_name='Тип')
    price = models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Цена')
    user_name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        db_table = 'product_entry_exit'
        ordering = ('-created_at',)
        verbose_name = 'Учет товара'
        verbose_name_plural = 'Учет товаров'

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.user_name = self.user.username
        super().save(*args, **kwargs)


class Release(models.Model):
    pk = models.CompositePrimaryKey("version", "name")
    version = models.IntegerField()
    name = models.CharField(max_length=20)