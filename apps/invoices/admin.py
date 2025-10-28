from django.contrib import admin
from .models import Invoice, InvoiceItem, InvoicePayment

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['numero', 'cliente', 'fecha', 'vencimiento', 'total', 'estado']
    list_filter = ['estado', 'fecha']
    search_fields = ['numero', 'cliente__nombre']

@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ['factura', 'producto', 'cantidad', 'precio_unitario']

@admin.register(InvoicePayment)
class InvoicePaymentAdmin(admin.ModelAdmin):
    list_display = ['factura', 'fecha_pago', 'metodo_pago']
