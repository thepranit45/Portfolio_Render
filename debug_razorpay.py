#!/usr/bin/env python
import os
import sys
import django
import requests

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
django.setup()

from django.conf import settings
import razorpay

def test_razorpay_api_directly():
    """Test Razorpay API directly using HTTP requests"""
    print('🔍 Testing Razorpay API directly...')
    
    import base64
    
    # Create basic auth header
    auth_string = f"{settings.RAZORPAY_KEY_ID}:{settings.RAZORPAY_KEY_SECRET}"
    auth_bytes = auth_string.encode('ascii')
    auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
    
    headers = {
        'Authorization': f'Basic {auth_b64}',
        'Content-Type': 'application/json'
    }
    
    # Test order creation
    order_data = {
        'amount': 1000,  # ₹10 in paise
        'currency': 'INR',
        'receipt': f'direct_test_{int(__import__("time").time())}'
    }
    
    try:
        response = requests.post(
            'https://api.razorpay.com/v1/orders',
            json=order_data,
            headers=headers,
            timeout=30
        )
        
        print(f'Status Code: {response.status_code}')
        print(f'Response: {response.text}')
        
        if response.status_code == 200:
            order = response.json()
            print('✅ Direct API call successful!')
            print(f'Order ID: {order["id"]}')
            return True
        else:
            print('❌ Direct API call failed!')
            return False
            
    except Exception as e:
        print(f'❌ API request error: {e}')
        return False

def test_key_format():
    """Test if the keys are in correct format"""
    print('\n🔍 Testing key format...')
    
    key_id = settings.RAZORPAY_KEY_ID
    key_secret = settings.RAZORPAY_KEY_SECRET
    
    print(f'Key ID: {key_id}')
    print(f'Key ID length: {len(key_id)}')
    print(f'Key ID starts with rzp_test_: {key_id.startswith("rzp_test_")}')
    
    print(f'Secret length: {len(key_secret)}')
    print(f'Secret format (first 8 chars): {key_secret[:8]}')
    
    # Check if keys are not default values
    if key_id == 'rzp_test_your_key_id' or key_secret == 'your_key_secret':
        print('❌ Keys are still default values!')
        return False
    
    if len(key_id) < 20 or len(key_secret) < 20:
        print('❌ Keys seem too short!')
        return False
        
    print('✅ Key format looks correct')
    return True

if __name__ == '__main__':
    print('🚀 Starting Detailed Razorpay Diagnostics...\n')
    
    # Test 1: Key format
    format_ok = test_key_format()
    
    # Test 2: Direct API call
    api_ok = test_razorpay_api_directly()
    
    print('\n📋 Diagnostic Summary:')
    print(f'  Key Format: {"✅ PASS" if format_ok else "❌ FAIL"}')
    print(f'  Direct API: {"✅ PASS" if api_ok else "❌ FAIL"}')
    
    if format_ok and api_ok:
        print('\n🎉 Razorpay configuration is correct!')
        print('If payments are still failing, check:')
        print('  1. Browser console for JavaScript errors')
        print('  2. Django logs during payment attempt')
        print('  3. Network requests in browser dev tools')
    else:
        print('\n🚨 Razorpay configuration has issues!')