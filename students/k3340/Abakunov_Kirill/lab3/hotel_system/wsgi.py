"""
WSGI config for hotel_system project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_system.settings')

application = get_wsgi_application()
