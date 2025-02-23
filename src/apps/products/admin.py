from django.contrib import admin
from django.contrib.admin.filters import RelatedOnlyFieldListFilter
from apps.products.models import Product, ProductInventoryOperation


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'count')
    readonly_fields = ('count', 'price')
    fields = ('name',)
    search_fields = ('name',)

    def price(self, obj):
        return obj.price

    def count(self, obj):
        return obj.count

    price.short_description = "Цена"
    count.short_description = "Кол-во"


@admin.register(ProductInventoryOperation)
class ProductInventoryOperationAdmin(admin.ModelAdmin):
    list_display = ('product', 'operation_type', 'count', 'price', 'user', 'created_at')
    fields = ('product', 'operation_type', 'count', 'price', 'user')
    readonly_fields = ('user',)
    list_filter = ('operation_type', 'user', 'created_at', ('product', RelatedOnlyFieldListFilter))
    search_fields = ('product__name',)
    autocomplete_fields = ('product',)
    actions = None

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)
