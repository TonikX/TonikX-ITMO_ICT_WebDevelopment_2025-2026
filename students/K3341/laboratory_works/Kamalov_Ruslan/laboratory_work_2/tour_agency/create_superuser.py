import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tour_agency.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin'
    )
    print('Superuser "admin" created successfully')
else:
    print('Superuser "admin" already exists')