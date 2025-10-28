from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Invoice
from .forms import InvoiceForm

# Lista simple de facturas
class InvoiceListView(ListView):
    model = Invoice
    template_name = 'invoices/invoice_list.html'

# Ver detalles de una factura
class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = 'invoices/invoice_detail.html'

# Crear nueva factura
class InvoiceCreateView(CreateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'invoices/invoice_form.html'
    success_url = reverse_lazy('invoices:invoice_list')

# Editar factura existente
class InvoiceUpdateView(UpdateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'invoices/invoice_form.html'
    success_url = reverse_lazy('invoices:invoice_list')
