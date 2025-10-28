from django.db import models

class Invoice(models.Model):
    ESTADOS_FACTURA = [
        ('borrador', '📝 Borrador'),
        ('enviada', '📤 Enviada'),
        ('pagada', '✅ Pagada'),
    ]
    
    numero = models.CharField(max_length=20, unique=True, verbose_name="🧾 Número")
    cliente = models.ForeignKey('clients.Client', on_delete=models.CASCADE, verbose_name="👥 Cliente")  #FOREIGNKEY
    fecha = models.DateField(verbose_name="📅 Fecha")
    vencimiento = models.DateField(verbose_name="⏰ Vencimiento")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="💰 Subtotal")
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="🏛️ IVA")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="💳 Total")
    estado = models.CharField(max_length=20, choices=ESTADOS_FACTURA, default='borrador', verbose_name="🎯 Estado")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="📅 Fecha de creación")

    class Meta:
        verbose_name = "🧾 Factura"
        verbose_name_plural = "🧾 Facturas"

    def __str__(self):
        return f"🧾 Factura {self.numero}"

#ONEtoONE RELATION
class InvoicePayment(models.Model):
    factura = models.OneToOneField(Invoice, on_delete=models.CASCADE, related_name='pago')
    fecha_pago = models.DateField(verbose_name="💳 Fecha de pago")
    metodo_pago = models.CharField(max_length=50, verbose_name="💳 Método de pago")
    referencia = models.CharField(max_length=100, blank=True, verbose_name="🔗 Referencia")

    def __str__(self):
        return f"💳 Pago de {self.factura.numero}"

class InvoiceItem(models.Model):
    #FOREIGNKEY (ya existía)
    factura = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items', verbose_name="🧾 Factura")
    producto = models.ForeignKey('products.Product', on_delete=models.CASCADE, verbose_name="📦 Producto")
    cantidad = models.IntegerField(default=1, verbose_name="📊 Cantidad")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="💰 Precio unitario")

    class Meta:
        verbose_name = "📋 Item de Factura"
        verbose_name_plural = "📋 Items de Factura"

    def __str__(self):
        return f"📦 {self.producto.nombre} x{self.cantidad}"
    
    @property
    def precio_total(self):
        return self.cantidad * self.precio_unitario
