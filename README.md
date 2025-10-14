                                                                       InvoiceApp Sistema de Reconocimiento Inteligente de Facturas

InvoiceApp es una aplicación web desarrollada en Django y Python diseñada específicamente para empresas del sector sanitario. El sistema permite automatizar el procesamiento de facturas mediante inteligencia artificial, reconociendo automáticamente productos sanitarios como lavabos, duchas y sanitarios.

**Objetivo del Proyecto**

Automatizar completamente la gestión documental de empresas sanitarias, reduciendo el tiempo de procesamiento de facturas en un 80% y minimizando errores humanos en la digitación de información.


**Características Principales**

**Reconocimiento Inteligente**
- Subir facturas en formato imagen o PDF
- Reconocer texto mediante tecnología OCR (Reconocimiento Óptico de Caracteres)
- Extraer información automáticamente (datos del cliente, montos, fechas)
- Almacenar en base de datos los datos estructurados
- Visualizar resultados mediante una interfaz web intuitiva
  

**Gestión Integral**
- Catálogo de productos sanitarios organizado
- Gestión de clientes y proveedores
- Seguimiento de stock en tiempo real
- Panel administrativo completo
  

**Experiencia Web**
- Interfaz web responsive optimizada para desktop
- Navegación intuitiva entre módulos
- Formularios web para gestión de productos
- Dashboard administrativo con métricas clave

**Tecnologías Utilizadas**
- Backend: Django 4.x, Python 3.9+
- OCR: Tesseract, OpenCV, Pillow
- Base de datos: PostgreSQL, Redis
- Frontend: HTML5, CSS3, JavaScript
- Procesamiento: Celery (para tareas asíncronas)
- Frontend: HTML5, CSS3, JavaScript, Bootstrap
- Contenedores: Docker, Docker Compose
  

**Funcionalidades Implementadas**
- Reconocimiento de texto con Tesseract OCR
- Procesamiento de imágenes con OpenCV
- Extracción de patrones (emails, teléfonos, montos)
- interfaz web responsive con Django
- Gestión de clientes automática
- Almacenamiento seguro de documentos
- Procesamiento asíncrono con Celery y Redis

  
**Arquitectura del Sistema**

Cliente →    Django Web  →   Procesamiento OCR  →    Base de datos
   ↓              ↓                ↓                     ↓
 Interfaz     Validación      Extracción AI          Almacenamiento
   Web          de datos        de datos             estructurado



**Módulos Principales**

**Procesamiento de Facturas**
- Subida mediante interfaz web drag & drop
- Reconocimiento automático de productos sanitarios
- Extracción de datos de clientes
- Validación y corrección manual desde el navegador

**Gestión de Productos**
- Formularios web para lavabos, duchas y sanitarios
- Control de inventario automático
- Categorización inteligente
- Gestión de precios y stock

**Administración de Clientes**
- Base de datos centralizada de clientes
- Historial de compras por cliente
- Segmentación y análisis comercial

**Dashboard Web**
- Métricas de procesamiento de documentos
- Estadísticas de ventas por producto
- Tendencias y reportes comerciales

**Arquitectura Web**
- Frontend Web: Interfaz de usuario en HTML,CSS y JavaScript
- Backend Django: Lógica de negocio y APIs
- Base de Datos: PostgreSQL para almacenamiento
- Servicios: OCR y procesamiento asíncrono


**Instalación y Configuración**

**Prerrequisitos**

Instalar Tesseract OCR
Ubuntu/Debian:
sudo apt-get install tesseract-ocr tesseract-ocr-fra

Windows:
Descargar desde: https://github.com/UB-Mannheim/tesseract/wiki
Crear un entorno virtual
python -m venv venv


**Instalación de Dependencias**

pip install -r requirements.txt


