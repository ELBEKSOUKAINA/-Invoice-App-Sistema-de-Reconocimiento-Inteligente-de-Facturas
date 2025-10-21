from django.contrib import admin
from .models import Category, Product, ProductSupplier

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_type', 'category', 'price', 'stock', 'is_active']
    list_filter = ['product_type', 'category', 'is_active']
    search_fields = ['name', 'sku']

@admin.register(ProductSupplier)
class ProductSupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_email', 'phone']
    search_fields = ['name']

