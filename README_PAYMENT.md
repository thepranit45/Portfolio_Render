# Razorpay Payment Integration Guide

## Overview
This Django portfolio website now includes a complete Razorpay payment gateway integration for accepting payments for services like consultations, development work, training, and maintenance.

## Features Implemented

### ✅ Core Payment System
- **Service Management**: Create and manage different types of services
- **Order Creation**: Generate orders with unique IDs and Razorpay integration  
- **Secure Payments**: PCI-compliant payment processing through Razorpay
- **Payment Verification**: Server-side signature verification for security
- **Order Tracking**: Complete order and payment history
- **Email Notifications**: Automatic confirmation emails

### ✅ User Interface
- **Services Catalog**: Professional service listing page
- **Payment Forms**: Multi-step payment process with validation
- **Razorpay Checkout**: Integrated payment gateway with multiple payment methods
- **Success/Failure Pages**: Complete payment flow handling
- **Responsive Design**: Mobile-friendly payment interface

### ✅ Admin Features  
- **Django Admin Integration**: Manage services, orders, and payments
- **Payment Analytics**: View payment statistics and order details
- **Service Management**: Easy CRUD operations for services
- **Customer Management**: Track customer orders and payments

## Directory Structure

```
portfolio_site/
├── portfolio/
│   ├── models.py           # PaymentOrder, Payment, Service models
│   ├── forms.py            # PaymentForm, ServiceForm
│   ├── views.py            # Payment views and webhook handlers
│   ├── urls.py             # Payment URLs
│   ├── admin.py            # Admin interface for payment models
│   ├── templates/portfolio/
│   │   ├── services.html           # Services catalog
│   │   ├── payment_form.html       # Customer details form
│   │   ├── payment_checkout.html   # Razorpay integration
│   │   ├── payment_success.html    # Success page
│   │   └── payment_failure.html    # Failure page
│   └── management/commands/
│       └── create_sample_services.py  # Sample data creation
├── requirements.txt        # Updated with razorpay dependency
├── .env.example           # Environment variables template
└── README_PAYMENT.md      # This file
```

## Database Models

### Service Model
- **Fields**: name, description, service_type, price, currency, duration, is_active
- **Types**: consultation, development, maintenance, training, other
- **Features**: Active/inactive toggle, pricing in multiple currencies

### PaymentOrder Model  
- **Fields**: order_id, razorpay_order_id, customer details, amount, status
- **Status**: created, pending, paid, failed, cancelled
- **Features**: UUID order IDs, JSON metadata support

### Payment Model
- **Fields**: razorpay_payment_id, order reference, amount, status, method
- **Status**: created, authorized, captured, refunded, failed  
- **Features**: Complete Razorpay response storage, payment verification

## API Endpoints

### Public URLs
- `/services/` - Service catalog page
- `/payment/create/<service_id>/` - Payment form
- `/payment/success/<order_id>/` - Payment success
- `/payment/failure/` - Payment failure  

### Internal URLs
- `/payment/callback/` - Razorpay payment callback (POST)
- `/payment/webhook/` - Razorpay webhooks (POST)

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your Razorpay credentials
RAZORPAY_KEY_ID=rzp_test_your_key_id
RAZORPAY_KEY_SECRET=your_test_key_secret
RAZORPAY_WEBHOOK_SECRET=your_webhook_secret
```

### 3. Database Setup
```bash
python manage.py makemigrations portfolio
python manage.py migrate
```

### 4. Create Sample Services
```bash
python manage.py create_sample_services
```

### 5. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

## Razorpay Configuration

### Test Mode Setup
1. **Create Razorpay Account**: Sign up at https://razorpay.com
2. **Get Test API Keys**: Dashboard → Settings → API Keys
3. **Configure Webhooks**: Dashboard → Settings → Webhooks
   - URL: `https://yoursite.com/payment/webhook/`
   - Events: `payment.captured`, `payment.failed`

### Webhook Configuration
```
Webhook URL: https://yoursite.com/payment/webhook/
Active Events:
- payment.captured
- payment.failed  
- order.paid
Secret: your_webhook_secret
```

## Payment Flow

### 1. Service Selection
- User browses services at `/services/`
- Clicks "Get Started" on desired service
- Redirected to payment form

### 2. Order Creation  
- User fills customer details form
- Order created in database with unique ID
- Razorpay order created via API

### 3. Payment Processing
- Razorpay checkout modal opens
- User completes payment with preferred method
- Payment response sent to callback endpoint

### 4. Verification & Completion
- Server verifies payment signature
- Order and payment records updated
- User redirected to success/failure page
- Confirmation email sent

## Security Features

### Payment Verification
- **Signature Validation**: Server-side verification of Razorpay signatures
- **Order Matching**: Strict order ID validation  
- **Amount Verification**: Ensure payment amount matches order
- **Duplicate Prevention**: Prevent double processing

### Data Protection
- **Encrypted Storage**: Sensitive data encrypted at rest
- **CSRF Protection**: All forms protected against CSRF attacks
- **SQL Injection**: Django ORM prevents SQL injection
- **XSS Protection**: Template auto-escaping enabled

## Error Handling

### Payment Failures
- **Network Issues**: Automatic retry mechanisms
- **Invalid Cards**: Clear error messages to users
- **Insufficient Funds**: Proper error handling
- **Bank Declines**: Fallback payment options

### System Errors
- **Database Errors**: Graceful degradation
- **API Failures**: Comprehensive error logging
- **Webhook Issues**: Retry mechanisms implemented
- **Email Failures**: Non-blocking email sending

## Testing

### Test Mode
- Use Razorpay test API keys
- Test cards available in Razorpay documentation
- No real money transactions in test mode

### Test Cards
```
Success: 4111 1111 1111 1111
Failure: 4000 0000 0000 0002
Insufficient Funds: 4000 0000 0000 9995
```

## Production Deployment

### Environment Variables
```bash
# Production settings
DEBUG=False
RAZORPAY_KEY_ID=rzp_live_your_key_id
RAZORPAY_KEY_SECRET=your_live_key_secret
DATABASE_URL=postgres://user:password@localhost/dbname
```

### Security Checklist
- [ ] Use live Razorpay API keys
- [ ] Configure SSL certificate
- [ ] Set DEBUG=False
- [ ] Configure proper ALLOWED_HOSTS  
- [ ] Set up webhook endpoints
- [ ] Configure email backend
- [ ] Set up monitoring and logging

## Customization

### Adding New Service Types
```python
# In models.py
SERVICE_TYPES = [
    ('consultation', 'Technical Consultation'),
    ('development', 'Custom Development'),
    ('maintenance', 'Website Maintenance'),
    ('training', 'Training Session'),
    ('your_new_type', 'Your New Service'),  # Add here
]
```

### Custom Payment Amounts
```python
# Allow custom pricing
service_form.fields['custom_amount'] = forms.DecimalField(
    max_digits=10, decimal_places=2, required=False
)
```

### Email Templates
- Customize email templates in `portfolio/templates/email/`
- Edit success/failure page content
- Add company branding and styling

## Monitoring & Analytics

### Payment Metrics
- Track conversion rates
- Monitor failed payments  
- Analyze popular services
- Customer analytics

### Error Monitoring
- Set up error tracking (Sentry)
- Monitor webhook delivery
- Track API response times
- Alert on payment failures

## Support & Troubleshooting

### Common Issues

1. **Payment Callback Not Working**
   - Check CSRF token configuration
   - Verify webhook URL accessibility
   - Check server logs for errors

2. **Signature Verification Failures**
   - Ensure correct API keys
   - Check webhook secret configuration
   - Verify callback data format

3. **Order Amount Mismatch**
   - Check currency configuration
   - Verify amount calculation (paise conversion)
   - Review tax/fee additions

### Debug Mode
Enable Django debug mode and check:
- Server logs for detailed error messages
- Database queries for optimization
- Email backend for delivery issues

## Contact & Support

For technical support or customization requests:
- **Email**: support@pranit-mestry.com
- **WhatsApp**: +91 9876543210
- **GitHub**: https://github.com/thepranit45

---

## Change Log

**v1.0.0** (November 18, 2025)
- Initial Razorpay integration
- Complete payment flow implementation
- Service management system
- Admin interface integration
- Comprehensive error handling
- Email notification system