from django.contrib import admin
from .models import Client, ClientProfile, ClientCategory

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'telefono', 'tipo', 'activo']
    list_filter = ['tipo', 'activo', 'fecha_creacion']
    search_fields = ['nombre', 'email']

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'fecha_registro']

@admin.register(ClientCategory)
class ClientCategoryAdmin(admin.ModelAdmin):
    list_display = ['nombre']
