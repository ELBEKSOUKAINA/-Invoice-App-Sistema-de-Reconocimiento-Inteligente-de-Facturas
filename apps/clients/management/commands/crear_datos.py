from django.core.management.base import BaseCommand
from apps.clients.models import Client
from apps.products.models import Product
from apps.invoices.models import Invoice, InvoiceItem

class Command(BaseCommand):
    help = 'Crear datos de prueba simples'

    def handle(self, *args, **options):
        print("Creando datos de prueba...")
        
        # Crear 2 clientes
        c1 = Client.objects.create(
            nombre="María López",
            email="maria@email.com"
        )
        
        c2 = Client.objects.create(
            nombre="Juan Pérez", 
            email="juan@email.com"
        )
        
        # Crear 2 productos
        p1 = Product.objects.create(
            nombre="Lavabo",
            codigo="LAV-100",
            precio=100.00
        )
        
        p2 = Product.objects.create(
            nombre="Grifo",
            codigo="GRIF-200", 
            precio=50.00
        )
        
        # Crear 1 factura con formato de fecha español
        factura = Invoice.objects.create(
            numero="FACT-300",
            cliente=c1,
            fecha="2024-01-20",  # Django maneja el formato internamente
            vencimiento="2024-02-20",
            total=150.00,
            estado="pagada"
        )
        
        # Agregar productos a la factura
        InvoiceItem.objects.create(
            factura=factura,
            producto=p1,
            cantidad=1,
            precio_unitario=p1.precio
        )
        
        print(" ¡Listo!")
        print(f" Clientes: {c1.nombre}, {c2.nombre}")
        print(f" Productos: {p1.nombre}, {p2.nombre}")
        print(f" Factura: {factura.numero} - ${factura.total}")
        print(f" Fecha: {factura.fecha.strftime('%d/%m/%Y')}")  
