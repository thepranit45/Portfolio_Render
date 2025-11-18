from django.contrib import admin
from .models import Contact, PaymentOrder, Payment, Service, Project


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name','email','created_at','responded')
    list_filter = ('responded','created_at')
    search_fields = ('name','email','message')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'is_featured', 'is_published', 'display_order', 'created_at')
    list_filter = ('category', 'status', 'is_featured', 'is_published', 'created_at')
    search_fields = ('title', 'description', 'technologies')
    list_editable = ('is_featured', 'is_published', 'display_order')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('display_order', '-created_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'short_description', 'description')
        }),
        ('Project Details', {
            'fields': ('category', 'status', 'technologies')
        }),
        ('Media & Links', {
            'fields': ('image', 'demo_url', 'github_url')
        }),
        ('Display Options', {
            'fields': ('is_featured', 'is_published', 'display_order')
        }),
    )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_type', 'price', 'currency', 'is_active', 'created_at')
    list_filter = ('service_type', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('price', 'is_active')
    ordering = ('service_type', 'name')


@admin.register(PaymentOrder)
class PaymentOrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer_name', 'customer_email', 'amount', 'currency', 'status', 'created_at')
    list_filter = ('status', 'currency', 'created_at')
    search_fields = ('order_id', 'customer_name', 'customer_email', 'razorpay_order_id')
    readonly_fields = ('order_id', 'razorpay_order_id', 'created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('razorpay_payment_id', 'order', 'amount', 'currency', 'status', 'method', 'created_at')
    list_filter = ('status', 'method', 'currency', 'created_at')
    search_fields = ('razorpay_payment_id', 'razorpay_order_id', 'order__order_id', 'order__customer_email')
    readonly_fields = ('razorpay_payment_id', 'razorpay_order_id', 'razorpay_signature', 'created_at', 'updated_at', 'captured_at')
    ordering = ('-created_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order')
