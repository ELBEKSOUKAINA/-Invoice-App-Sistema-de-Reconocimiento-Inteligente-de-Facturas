from django.contrib import admin
from .models import Invoice, InvoiceItem

class InvoiceItemInline(admin.TabularInline):
    """Items de factura en línea"""
    model = InvoiceItem
    extra = 1
    readonly_fields = ['total_price']

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'client', 'invoice_date', 'due_date', 'total', 'status']
    list_filter = ['status', 'invoice_date', 'client']
    search_fields = ['invoice_number', 'client__name']
    readonly_fields = ['subtotal', 'tax_amount', 'total', 'created_at', 'updated_at']
    inlines = [InvoiceItemInline]
    date_hierarchy = 'invoice_date'

@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'product', 'quantity', 'unit_price', 'total_price']
    list_filter = ['invoice__invoice_date']
    search_fields = ['invoice__invoice_number', 'product__name']
