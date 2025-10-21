from django.shortcuts import render
from .models import Invoice

def invoice_list(request):
    """Vista básica para listar facturas"""
    invoices = Invoice.objects.all()
    return render(request, 'invoices/invoice_list.html', {'invoices': invoices})

def invoice_detail(request, invoice_id):
    """Vista básica para ver detalle de factura"""
    invoice = Invoice.objects.get(id=invoice_id)
    return render(request, 'invoices/invoice_detail.html', {'invoice': invoice})
