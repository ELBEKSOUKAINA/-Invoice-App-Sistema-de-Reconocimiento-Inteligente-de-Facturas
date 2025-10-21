from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from apps.clients.models import Client
from apps.products.models import Product

class Invoice(models.Model):
    """Modelo para facturas"""
    
    INVOICE_STATUS_CHOICES = [
        ('draft', '📝 Borrador'),
        ('sent', '📤 Enviada'),
        ('paid', '✅ Pagada'),
        ('cancelled', '❌ Cancelada'),
    ]
    
    # Información básica
    invoice_number = models.CharField(max_length=50, unique=True, verbose_name="Número de Factura")
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name='invoices',
        verbose_name="Cliente"
    )
    invoice_date = models.DateField(verbose_name="Fecha de Factura")
    due_date = models.DateField(verbose_name="Fecha de Vencimiento")
    
    # Totales
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Subtotal"
    )
    tax_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Impuestos"
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Total"
    )
    
    # Estado
    status = models.CharField(
        max_length=20,
        choices=INVOICE_STATUS_CHOICES,
        default='draft',
        verbose_name="Estado"
    )
    
    # Control
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    
    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
        ordering = ['-invoice_date', '-created_at']
    
    def __str__(self):
        return f"Factura {self.invoice_number} - {self.client.name}"
    
    def save(self, *args, **kwargs):
        """Generar número de factura automáticamente si no existe"""
        if not self.invoice_number:
            last_invoice = Invoice.objects.order_by('-id').first()
            last_number = int(last_invoice.invoice_number.split('-')[-1]) if last_invoice else 0
            self.invoice_number = f"FACT-{last_number + 1:04d}"
        super().save(*args, **kwargs)

class InvoiceItem(models.Model):
    """Items de la factura"""
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Factura"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name="Producto"
    )
    quantity = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name="Cantidad"
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Precio Unitario"
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Precio Total"
    )
    
    class Meta:
        verbose_name = "Item de Factura"
        verbose_name_plural = "Items de Factura"
    
    def __str__(self):
        return f"{self.product.name} x{self.quantity}"
    
    def save(self, *args, **kwargs):
        """Calcular el precio total automáticamente"""
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
