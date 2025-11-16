import os
import sys
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
try:
    import django
    django.setup()
    from django.urls import reverse
    try:
        print('reverse:', reverse('portfolio:project_student_result'))
    except Exception:
        print('Reverse failed:')
        traceback.print_exc()
    # list names in resolver for quick inspection
    from django.urls import get_resolver
    resolver = get_resolver(None)
    names = sorted([k for k in resolver.reverse_dict.keys() if isinstance(k, str)])
    print('\nRegistered url names (sample):')
    for n in names[:200]:
        print(' -', n)
except Exception:
    print('Error importing Django/settings:')
    traceback.print_exc()
