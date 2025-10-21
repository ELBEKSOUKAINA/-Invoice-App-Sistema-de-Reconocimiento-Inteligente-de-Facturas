from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Category(models.Model):
    """Categorías para productos sanitarios"""
    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Product(models.Model):
    """Productos sanitarios: lavabos, duchas, sanitarios"""
    
    # Choices para tipos de productos sanitarios
    PRODUCT_TYPE_CHOICES = [
        ('sink', '🛁 Lavabo'),
        ('shower', '🚿 Ducha'),
        ('toilet', '🚽 Sanitario'),
        ('faucet', '⚙️ Grifería'),
        ('accessory', '🔧 Accesorio'),
    ]
    
    # Información básica
    name = models.CharField(max_length=200, verbose_name="Nombre del Producto")
    description = models.TextField(blank=True, verbose_name="Descripción")
    
    # ✅ FOREIGNKEY con Category
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='products',
        verbose_name="Categoría"
    )
    
    # Especificaciones
    product_type = models.CharField(
        max_length=20,
        choices=PRODUCT_TYPE_CHOICES,
        default='sink',
        verbose_name="Tipo de Producto"
    )
    
    # Precios y stock
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Precio"
    )
    
    stock = models.IntegerField(default=0, verbose_name="Stock")
    sku = models.CharField(max_length=50, unique=True, verbose_name="SKU")
    
    # Control
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - ${self.price}"

class ProductSupplier(models.Model):
    """Proveedores de productos"""
    name = models.CharField(max_length=200, verbose_name="Nombre del Proveedor")
    contact_email = models.EmailField(blank=True, verbose_name="Email de Contacto")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")  
    
    # ✅ MANYTOMANY con Product
    products = models.ManyToManyField(
        Product,
        related_name='suppliers',
        verbose_name="Productos"
    )
    
    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
    
    def __str__(self):
        return self.name

# ✅ ONETOONE (Ejemplo adicional)
class ProductDetail(models.Model):
    """Información detallada del producto - Relación OneToOne"""
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name='details',
        verbose_name="Producto"
    )
    dimensions = models.CharField(max_length=100, blank=True, verbose_name="Dimensiones")
    material = models.CharField(max_length=100, blank=True, verbose_name="Material")
    warranty_months = models.IntegerField(default=12, verbose_name="Meses de Garantía")
    
    class Meta:
        verbose_name = "Detalle de Producto"
        verbose_name_plural = "Detalles de Producto"
    
    def __str__(self):
        return f"Detalles de {self.product.name}"
