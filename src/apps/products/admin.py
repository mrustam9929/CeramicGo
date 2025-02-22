from django.contrib import admin

from apps.products.models import Product, ProductInventoryOperation


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'count')
    readonly_fields = ('count', )
    fields = ('name',)


@admin.register(ProductInventoryOperation)
class ProductInventoryOperationAdmin(admin.ModelAdmin):
    pass
    # list_display = ('product', 'operation_type', 'count', 'price')
    # fields = ('product', 'operation_type', 'count', 'price')
