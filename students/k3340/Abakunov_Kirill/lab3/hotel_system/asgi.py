"""
ASGI config for hotel_system project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_system.settings')

application = get_asgi_application()
