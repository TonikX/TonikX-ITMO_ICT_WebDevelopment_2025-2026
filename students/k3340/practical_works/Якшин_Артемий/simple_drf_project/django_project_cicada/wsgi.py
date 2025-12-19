"""
WSGI config for django_project_cicada project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project_cicada.settings')

application = get_wsgi_application()


