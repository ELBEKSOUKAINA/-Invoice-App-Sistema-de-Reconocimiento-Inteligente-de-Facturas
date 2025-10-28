from django.urls import path
from .views import InvoiceListView, InvoiceDetailView, InvoiceCreateView, InvoiceUpdateView

app_name = 'invoices'

urlpatterns = [
    path('', InvoiceListView.as_view(), name='invoice_list'),
    path('<int:pk>/', InvoiceDetailView.as_view(), name='invoice_detail'),
    path('new/', InvoiceCreateView.as_view(), name='invoice_create'),
    path('<int:pk>/edit/', InvoiceUpdateView.as_view(), name='invoice_edit'),
]
