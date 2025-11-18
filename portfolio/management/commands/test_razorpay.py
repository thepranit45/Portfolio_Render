from django.core.management.base import BaseCommand
from django.conf import settings
import razorpay


class Command(BaseCommand):
    help = 'Test Razorpay connection and configuration'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔍 Testing Razorpay Configuration...'))
        
        # Check settings
        self.stdout.write(f"Key ID: {settings.RAZORPAY_KEY_ID}")
        self.stdout.write(f"Key Secret: {settings.RAZORPAY_KEY_SECRET[:8]}...")
        
        try:
            # Initialize client
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            self.stdout.write(self.style.SUCCESS('✅ Razorpay client initialized'))
            
            # Test creating an order
            order_data = {
                'amount': 99900,  # ₹999 in paise
                'currency': 'INR',
                'receipt': 'test_receipt_' + str(int(1000000000))
            }
            
            order = client.order.create(data=order_data)
            self.stdout.write(self.style.SUCCESS('✅ Test order created successfully'))
            self.stdout.write(f"Order ID: {order['id']}")
            self.stdout.write(f"Amount: ₹{order['amount']/100}")
            self.stdout.write(f"Status: {order['status']}")
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: {e}'))
            self.stdout.write(self.style.ERROR('Check your Razorpay credentials'))