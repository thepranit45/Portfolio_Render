from django.db import models
import uuid
from django.utils.text import slugify


class Contact(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    responded = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} <{self.email}>"


class Project(models.Model):
    """Model to store portfolio projects"""
    CATEGORY_CHOICES = [
        ('web', 'Web Development'),
        ('mobile', 'Mobile Development'),
        ('iot', 'IoT Projects'),
        ('automation', 'Automation'),
        ('ai-ml', 'AI/ML'),
        ('education', 'Educational'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
        ('planned', 'Planned'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, help_text="Brief description for cards")
    
    # Project details
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='web')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    technologies = models.CharField(max_length=500, help_text="Comma separated list of technologies used")
    
    # Media
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    demo_url = models.URLField(blank=True, null=True, help_text="Live demo URL")
    github_url = models.URLField(blank=True, null=True, help_text="GitHub repository URL")
    
    # Display options
    is_featured = models.BooleanField(default=False, help_text="Show on homepage")
    is_published = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0, help_text="Lower numbers appear first")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['display_order', '-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_technologies_list(self):
        """Return technologies as a list"""
        if self.technologies:
            return [tech.strip() for tech in self.technologies.split(',')]
        return []


class PaymentOrder(models.Model):
    """Model to store payment orders"""
    CURRENCY_CHOICES = [
        ('INR', 'Indian Rupee'),
        ('USD', 'US Dollar'),
    ]
    
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    order_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=15, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='INR')
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional metadata
    notes = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.order_id} - {self.customer_name} - ₹{self.amount}"


class Payment(models.Model):
    """Model to store payment transactions"""
    PAYMENT_STATUS_CHOICES = [
        ('created', 'Created'),
        ('authorized', 'Authorized'),
        ('captured', 'Captured'),
        ('refunded', 'Refunded'),
        ('failed', 'Failed'),
    ]
    
    order = models.ForeignKey(PaymentOrder, on_delete=models.CASCADE, related_name='payments')
    razorpay_payment_id = models.CharField(max_length=100, unique=True)
    razorpay_order_id = models.CharField(max_length=100)
    razorpay_signature = models.CharField(max_length=500, blank=True, null=True)
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='INR')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='created')
    method = models.CharField(max_length=50, blank=True)  # card, netbanking, wallet, upi
    
    # Payment details
    captured_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional data from Razorpay
    payment_data = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Payment {self.razorpay_payment_id} - {self.status}"


class Service(models.Model):
    """Model to define services that can be purchased"""
    SERVICE_TYPES = [
        ('consultation', 'Technical Consultation'),
        ('development', 'Custom Development'),
        ('maintenance', 'Website Maintenance'),
        ('training', 'Training Session'),
        ('other', 'Other Services'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='INR')
    duration = models.CharField(max_length=100, blank=True)  # e.g., "1 hour", "1 week"
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['service_type', 'name']
    
    def __str__(self):
        return f"{self.name} - ₹{self.price}"
