from django.db import models
from django.core.validators import EmailValidator, RegexValidator
from django.utils import timezone

class Client(models.Model):
    """
    Model for managing clients of the sanitary products company
    Relationships:
    - ForeignKey: Invoice (an invoice belongs to one client)
    - OneToOne: Can be extended with ClientProfile if needed
    """
    
    # Choices for client types
    CLIENT_TYPE_CHOICES = [
        ('individual', '🧑 Individual'),
        ('professional', '👨‍💼 Professional'),
        ('company', '🏢 Company'),
        ('architect', '📐 Architect'),
        ('installer', '🔧 Installer'),
        ('distributor', '📦 Distributor'),
    ]
    
    # Validators
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be between 9 and 15 digits."
    )
    
    # === BASIC INFORMATION ===
    name = models.CharField(
        max_length=200, 
        verbose_name="Name/Company Name",
        help_text="Full name or company name of the client"
    )
    
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator()],
        verbose_name="Email Address",
        help_text="Primary contact email"
    )
    
    phone = models.CharField(
        max_length=20, 
        blank=True,
        validators=[phone_validator],
        verbose_name="Phone Number",
        help_text="Contact phone number"
    )
    
    # === CONTACT INFORMATION ===
    address = models.TextField(
        blank=True, 
        verbose_name="Address",
        help_text="Complete address"
    )
    
    city = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="City",
        default="Madrid"
    )
    
    postal_code = models.CharField(
        max_length=10, 
        blank=True, 
        verbose_name="Postal Code"
    )
    
    province = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Province",
        default="Madrid"
    )
    
    # === COMMERCIAL INFORMATION ===
    client_type = models.CharField(
        max_length=20,
        choices=CLIENT_TYPE_CHOICES,
        default='individual',
        verbose_name="Client Type",
        help_text="Select the client type"
    )
    
    tax_id = models.CharField(
        max_length=20, 
        blank=True, 
        verbose_name="Tax ID/CIF/NIF",
        help_text="Tax identification number"
    )
    
    # === SPECIFIC FIELDS FOR COMPANIES ===
    company_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Company Name",
        help_text="Official company name (if different)"
    )
    
    business_activity = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Business Activity",
        help_text="Main business activity"
    )
    
    # === PREFERENCES AND SEGMENTATION ===
    preferred_products = models.TextField(
        blank=True,
        verbose_name="Products of Interest",
        help_text="Sanitary products the client is interested in"
    )
    
    notes = models.TextField(
        blank=True,
        verbose_name="Internal Notes",
        help_text="Additional information about the client"
    )
    
    # === CONTROL FIELDS ===
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active",
        help_text="Indicates if the client is active"
    )
    
    is_vip = models.BooleanField(
        default=False,
        verbose_name="VIP Client",
        help_text="Client with preferential treatment"
    )
    
    credit_limit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Credit Limit",
        help_text="Credit limit assigned to the client"
    )
    
    # === DATES ===
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Creation Date"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Last Update"
    )
    
    last_purchase_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Last Purchase Date"
    )

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['email']),
            models.Index(fields=['client_type']),
            models.Index(fields=['is_active']),
            models.Index(fields=['created_at']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['email'],
                name='unique_client_email'
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_client_type_display()})"
    
    def get_full_address(self):
        """Returns the complete formatted address"""
        address_parts = []
        if self.address:
            address_parts.append(self.address)
        if self.city:
            address_parts.append(self.city)
        if self.postal_code:
            address_parts.append(self.postal_code)
        if self.province:
            address_parts.append(self.province)
        return ", ".join(address_parts) if address_parts else "No address specified"
    
    def get_display_name(self):
        """Display name, prioritizing company_name for companies"""
        if self.client_type == 'company' and self.company_name:
            return self.company_name
        return self.name
    
    @property
    def total_invoices_count(self):
        """Total number of invoices for the client"""
        from apps.invoices.models import Invoice
        return Invoice.objects.filter(client=self).count()
    
    @property
    def total_purchases_amount(self):
        """Total amount spent by the client"""
        from apps.invoices.models import Invoice
        from django.db.models import Sum
        result = Invoice.objects.filter(client=self).aggregate(
            total=Sum('total_amount')
        )
        return result['total'] or 0.00
    
    @property
    def needs_credit_review(self):
        """Indicates if the client needs credit review"""
        return self.total_purchases_amount > self.credit_limit * 0.8
    
    def update_last_purchase(self):
        """Updates the last purchase date"""
        from apps.invoices.models import Invoice
        last_invoice = Invoice.objects.filter(
            client=self
        ).order_by('-issue_date').first()
        
        if last_invoice:
            self.last_purchase_date = last_invoice.issue_date
            self.save(update_fields=['last_purchase_date'])


class ClientContact(models.Model):
    """
    Additional contacts for company clients
    Relationship: ForeignKey with Client
    """
    
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='contacts',
        verbose_name="Client"
    )
    
    name = models.CharField(
        max_length=100,
        verbose_name="Contact Name"
    )
    
    position = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Position/Title"
    )
    
    email = models.EmailField(
        blank=True,
        verbose_name="Contact Email"
    )
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')],
        verbose_name="Contact Phone"
    )
    
    department = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Department"
    )
    
    is_main_contact = models.BooleanField(
        default=False,
        verbose_name="Main Contact"
    )
    
    can_authorize_orders = models.BooleanField(
        default=False,
        verbose_name="Can Authorize Orders"
    )
    
    notes = models.TextField(
        blank=True,
        verbose_name="Contact Notes"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Client Contact"
        verbose_name_plural = "Client Contacts"
        ordering = ['client', '-is_main_contact', 'name']
        unique_together = ['client', 'email']

    def __str__(self):
        return f"{self.name} - {self.client.name}"


class ClientSegment(models.Model):
    """
    Client segmentation for marketing
    Relationship: ManyToMany with Client
    """
    
    SEGMENT_CHOICES = [
        ('frequent', '🔄 Frequent Client'),
        ('wholesale', '📦 Wholesaler'),
        ('retail', '🏪 Retailer'),
        ('contractor', '🔨 Contractor'),
        ('architect', '📐 Architecture Firm'),
        ('vip', '⭐ VIP Client'),
        ('new', '🆕 New Client'),
        ('inactive', '💤 Inactive Client'),
    ]
    
    name = models.CharField(
        max_length=50,
        choices=SEGMENT_CHOICES,
        unique=True,
        verbose_name="Segment Name"
    )
    
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    
    clients = models.ManyToManyField(
        Client,
        related_name='segments',
        blank=True,
        verbose_name="Clients"
    )
    
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        verbose_name="Discount %",
        help_text="Applicable discount percentage"
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active Segment"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Client Segment"
        verbose_name_plural = "Client Segments"
        ordering = ['name']

    def __str__(self):
        return self.get_name_display()
    
    def clients_count(self):
        return self.clients.count()
    
    clients_count.short_description = "Number of Clients"


# Signals for data integrity
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

@receiver(pre_save, sender=Client)
def update_company_info(sender, instance, **kwargs):
    """
    Automatically updates company_name for company clients
    """
    if instance.client_type == 'company' and not instance.company_name:
        instance.company_name = instance.name

@receiver(post_save, sender=Client)
def create_main_contact(sender, instance, created, **kwargs):
    """
    Automatically creates a main contact for new companies
    """
    if created and instance.client_type == 'company':
        ClientContact.objects.create(
            client=instance,
            name=instance.name,
            email=instance.email,
            phone=instance.phone,
            position="Main Contact",
            is_main_contact=True,
            can_authorize_orders=True
        )