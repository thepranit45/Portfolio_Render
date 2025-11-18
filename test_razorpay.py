#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
django.setup()

from django.conf import settings
import razorpay

def test_razorpay_connection():
    print('🔍 Testing Razorpay Connection...')
    print(f'Key ID: {settings.RAZORPAY_KEY_ID}')
    print(f'Secret: {settings.RAZORPAY_KEY_SECRET[:8]}...')
    
    try:
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        # Test order creation for Code Review Service (₹10)
        order_data = {
            'amount': 1000,  # ₹10 in paise
            'currency': 'INR',
            'receipt': f'test_code_review_{int(__import__("time").time())}'
        }
        
        order = client.order.create(data=order_data)
        print('✅ Order creation successful!')
        print(f'Order ID: {order["id"]}')
        print(f'Amount: ₹{order["amount"]/100}')
        print(f'Status: {order["status"]}')
        
        return True, order
        
    except Exception as e:
        print(f'❌ Razorpay Error: {e}')
        print(f'Error type: {type(e).__name__}')
        return False, str(e)

def test_payment_views():
    print('\n🔍 Testing Payment Views...')
    
    from portfolio.models import Service
    from django.test import Client
    from django.contrib.auth.models import User
    
    try:
        # Get Code Review Service
        code_review = Service.objects.get(name='Code Review Service')
        print(f'✅ Found service: {code_review.name} - ₹{code_review.price}')
        
        # Test client
        client = Client()
        
        # Test create payment view
        response = client.get(f'/payment/create/{code_review.id}/')
        print(f'Create payment response: {response.status_code}')
        
        if response.status_code == 200:
            print('✅ Payment creation page loads successfully')
        else:
            print(f'❌ Payment creation failed with status {response.status_code}')
            
        return True
        
    except Exception as e:
        print(f'❌ Payment view test error: {e}')
        return False

if __name__ == '__main__':
    print('🚀 Starting Razorpay Payment Test...\n')
    
    # Test 1: Razorpay API Connection
    api_success, api_result = test_razorpay_connection()
    
    # Test 2: Django Views
    view_success = test_payment_views()
    
    print('\n📋 Test Summary:')
    print(f'  Razorpay API: {"✅ PASS" if api_success else "❌ FAIL"}')
    print(f'  Payment Views: {"✅ PASS" if view_success else "❌ FAIL"}')
    
    if api_success and view_success:
        print('\n🎉 All tests passed! Payment system should work correctly.')
    else:
        print('\n🚨 Some tests failed. Check the errors above.')