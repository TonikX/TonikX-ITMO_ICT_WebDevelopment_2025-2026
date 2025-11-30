
from .base import *


DEBUG = True

ALLOWED_HOSTS = ["*"]

SECRET_KEY = "secret"  # noqa: S105

STATIC_URL = "/static/"
STATIC_ROOT = base_dir_join("static")

MEDIA_URL = "/media/"
MEDIA_ROOT = base_dir_join("media")


SESSION_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SAMESITE = "None"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

AUTH_PASSWORD_VALIDATORS = []

# Celery
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="")
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True


CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8082",
    "http://localhost:8082",
]

SESSION_COOKIE_DOMAIN = None
CSRF_COOKIE_DOMAIN = None
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

SECURE_SSL_REDIRECT = False

MAX_FILE_UPLOAD_MB = 50
ALLOWED_FILE_MIME_TYPE = [
    "image/jpeg",
    "image/png",
    "video/mp4",
    "application/pdf",
]