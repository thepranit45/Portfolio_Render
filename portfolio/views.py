from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views import View
import razorpay
import json
import uuid
import hmac
import hashlib

from .forms import ContactForm, PaymentForm
from .models import Contact, PaymentOrder, Payment, Service

def home(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        contact = form.save()
        # send email to DEFAULT_FROM_EMAIL (dev -> console)
        send_mail(
            subject=f"New contact from {contact.name}",
            message=contact.message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=True,
        )
        messages.success(request, "Thanks — your message was sent!")
        return redirect(reverse('portfolio:home') + '#contact')
    return render(request, 'portfolio/home.html', {'form': form})


def about(request):
    return render(request, 'portfolio/about.html')


def skills(request):
    return render(request, 'portfolio/skills.html')


def projects(request):
    return render(request, 'portfolio/projects.html')


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        contact = form.save()
        send_mail(
            subject=f"New contact from {contact.name}",
            message=contact.message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=True,
        )
        messages.success(request, "Thanks — your message was sent!")
        return redirect(reverse('portfolio:contact'))
    return render(request, 'portfolio/contact.html', {'form': form})


def project_student_result(request):
    """Project detail page for Student Result System (static page)."""
    # The template will contain Features, Technologies and Modules as requested
    return render(request, 'portfolio/project_student_result.html')


def project_attendance_management(request):
    """Project detail page for Attendance Management System (static page)."""
    return render(request, 'portfolio/project_attendance_management.html')


def project_detail(request, slug):
    """Generic project detail view. Looks up project data by slug and renders a detail page.

    We use a small in-memory map for content so we can render deep info pages without a DB.
    """
    projects = {
        'student-result': {
            'title': 'Student Result System',
            'short': 'Result management system with admin dashboard and automatic CGPA computation.',
            'features': [
                'Admin login & dashboard',
                'Add/manage students & subjects',
                'Enter marks and generate results',
                'Automatic CGPA, percentage & pass/fail calculation',
                'Students can view and download/print their results',
                'Secure and user-friendly interface',
            ],
            'technologies': {
                'frontend': 'HTML, CSS, JavaScript',
                'backend': 'PHP',
                'database': 'MySQL',
                'tools': 'XAMPP/WAMP, phpMyAdmin',
            },
            'modules': [
                'Admin Module: Manage students, subjects, marks, results',
                'Student Module: View & download result',
                'Result Module: CGPA, percentage, pass/fail processing',
            ],
        },
        # Add additional project slugs here as needed
    }

    project = projects.get(slug)
    if not project:
        raise Http404('Project not found')

    return render(request, 'portfolio/project_detail.html', {'project': project, 'slug': slug})


# Policy Pages Views
def privacy(request):
    """Privacy Policy page."""
    return render(request, 'portfolio/privacy.html')


def terms(request):
    """Terms and Conditions page."""
    return render(request, 'portfolio/terms.html')


def refund(request):
    """Cancellation and Refund Policy page."""
    return render(request, 'portfolio/refund.html')


def delivery(request):
    """Shipping and Delivery Policy page."""
    return render(request, 'portfolio/delivery.html')


# Payment Views
def services(request):
    """Display all available services."""
    services = Service.objects.filter(is_active=True)
    return render(request, 'portfolio/services.html', {'services': services})


def create_payment(request, service_id):
    """Create a payment order for a specific service."""
    service = get_object_or_404(Service, id=service_id, is_active=True)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Create PaymentOrder
            order = form.save(commit=False)
            order.amount = service.price
            order.currency = service.currency
            order.order_id = str(uuid.uuid4())[:8].upper()
            order.save()
            
            # Debug: Print Razorpay keys for troubleshooting
            print(f"DEBUG - RAZORPAY_KEY_ID: {settings.RAZORPAY_KEY_ID}")
            print(f"DEBUG - RAZORPAY_KEY_SECRET: {settings.RAZORPAY_KEY_SECRET[:8]}...")
            
            # Initialize Razorpay client
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            print("DEBUG - Razorpay client initialized successfully")
            
            # Create Razorpay order
            razorpay_order_data = {
                'amount': int(order.amount * 100),  # Amount in paise
                'currency': order.currency,
                'receipt': order.order_id,
                'notes': {
                    'service_id': service.id,
                    'service_name': service.name,
                    'customer_email': order.customer_email
                }
            }
            
            try:
                razorpay_order = client.order.create(data=razorpay_order_data)
                order.razorpay_order_id = razorpay_order['id']
                order.status = 'pending'
                order.save()
                
                context = {
                    'order': order,
                    'service': service,
                    'razorpay_order_id': razorpay_order['id'],
                    'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                    'amount': int(order.amount * 100),
                    'currency': order.currency,
                }
                return render(request, 'portfolio/payment_checkout.html', context)
                
            except Exception as e:
                messages.error(request, f"Payment initialization failed: {str(e)}")
                return redirect('portfolio:services')
    else:
        form = PaymentForm()
    
    return render(request, 'portfolio/payment_form.html', {
        'form': form,
        'service': service
    })


@csrf_exempt
@require_POST
def payment_callback(request):
    """Handle Razorpay payment callback."""
    try:
        # Get the payment data from the callback
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        
        # Verify the payment signature
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        # Create signature verification data
        generated_signature = hmac.new(
            key=settings.RAZORPAY_KEY_SECRET.encode('utf-8'),
            msg=(razorpay_order_id + "|" + razorpay_payment_id).encode('utf-8'),
            digestmod=hashlib.sha256
        ).hexdigest()
        
        if generated_signature == razorpay_signature:
            # Payment verified successfully
            try:
                # Get the order
                order = PaymentOrder.objects.get(razorpay_order_id=razorpay_order_id)
                
                # Create Payment record
                payment = Payment.objects.create(
                    order=order,
                    razorpay_payment_id=razorpay_payment_id,
                    razorpay_order_id=razorpay_order_id,
                    razorpay_signature=razorpay_signature,
                    amount=order.amount,
                    currency=order.currency,
                    status='captured'
                )
                
                # Update order status
                order.status = 'paid'
                order.save()
                
                # Send confirmation email
                send_mail(
                    subject=f"Payment Confirmation - Order {order.order_id}",
                    message=f"Dear {order.customer_name},\n\nYour payment of ₹{order.amount} has been successfully processed.\n\nOrder ID: {order.order_id}\nPayment ID: {razorpay_payment_id}\n\nThank you!",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[order.customer_email],
                    fail_silently=True,
                )
                
                return redirect('portfolio:payment_success', order_id=order.order_id)
                
            except PaymentOrder.DoesNotExist:
                return redirect('portfolio:payment_failure')
                
        else:
            # Signature verification failed
            return redirect('portfolio:payment_failure')
            
    except Exception as e:
        print(f"Payment callback error: {str(e)}")
        return redirect('portfolio:payment_failure')


def payment_success(request, order_id):
    """Payment success page."""
    try:
        order = PaymentOrder.objects.get(order_id=order_id, status='paid')
        payment = order.payments.first()
        return render(request, 'portfolio/payment_success.html', {
            'order': order,
            'payment': payment
        })
    except PaymentOrder.DoesNotExist:
        return redirect('portfolio:payment_failure')


def payment_failure(request):
    """Payment failure page."""
    return render(request, 'portfolio/payment_failure.html')


@csrf_exempt
def payment_webhook(request):
    """Handle Razorpay webhooks for payment status updates."""
    if request.method == 'POST':
        try:
            webhook_signature = request.META.get('HTTP_X_RAZORPAY_SIGNATURE')
            webhook_secret = settings.RAZORPAY_WEBHOOK_SECRET
            
            # Verify webhook signature
            if webhook_signature:
                generated_signature = hmac.new(
                    webhook_secret.encode('utf-8'),
                    request.body,
                    hashlib.sha256
                ).hexdigest()
                
                if generated_signature == webhook_signature:
                    # Process webhook data
                    webhook_data = json.loads(request.body)
                    event = webhook_data.get('event')
                    
                    if event == 'payment.captured':
                        # Handle payment captured event
                        payment_data = webhook_data['payload']['payment']['entity']
                        try:
                            payment = Payment.objects.get(
                                razorpay_payment_id=payment_data['id']
                            )
                            payment.status = 'captured'
                            payment.payment_data = payment_data
                            payment.save()
                        except Payment.DoesNotExist:
                            pass
                    
                    elif event == 'payment.failed':
                        # Handle payment failed event
                        payment_data = webhook_data['payload']['payment']['entity']
                        try:
                            order = PaymentOrder.objects.get(
                                razorpay_order_id=payment_data['order_id']
                            )
                            order.status = 'failed'
                            order.save()
                        except PaymentOrder.DoesNotExist:
                            pass
                    
                    return HttpResponse("OK")
                
        except Exception as e:
            print(f"Webhook error: {str(e)}")
    
    return HttpResponse("Invalid request", status=400)
