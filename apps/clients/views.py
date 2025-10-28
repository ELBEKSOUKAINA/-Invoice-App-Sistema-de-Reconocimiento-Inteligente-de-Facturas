from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Client
from .forms import ClientForm

# Lista simple de clientes
class ClientListView(ListView):
    model = Client
    template_name = 'clients/client_list.html'

# Ver detalles de un cliente
class ClientDetailView(DetailView):
    model = Client
    template_name = 'clients/client_detail.html'

# Crear nuevo cliente
class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('clients:client_list')

# Editar cliente existente
class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('clients:client_list')
