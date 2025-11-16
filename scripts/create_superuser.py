import os
import sys

# Ensure we run from project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')

import django
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

USERNAME = 'thepranit'
EMAIL = 'admin@example.com'
PASSWORD = 'thepranit'

try:
    user = User.objects.filter(username=USERNAME).first()
    if user:
        user.set_password(PASSWORD)
        user.is_superuser = True
        user.is_staff = True
        user.email = EMAIL
        user.save()
        print(f"Superuser '{USERNAME}' updated.")
    else:
        User.objects.create_superuser(username=USERNAME, email=EMAIL, password=PASSWORD)
        print(f"Superuser '{USERNAME}' created.")
except Exception as e:
    print('Error:', e)
    raise
