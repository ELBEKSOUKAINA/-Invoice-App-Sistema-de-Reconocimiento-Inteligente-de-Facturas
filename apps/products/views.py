from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Product
from .forms import ProductForm

# Lista simple de productos
class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'

# Ver detalles de un producto
class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'

# Crear nuevo producto
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('products:product_list')

# Editar producto existente
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('products:product_list')
