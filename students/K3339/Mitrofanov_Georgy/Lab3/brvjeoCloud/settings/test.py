from .base import *


SECRET_KEY = "test"  # nosec
DEBUG = True
ALLOWED_HOSTS = ["localhost"]

STATIC_ROOT = base_dir_join("staticfiles")
STATIC_URL = "/static/"

MEDIA_ROOT = base_dir_join("mediafiles/")
MEDIA_URL = "/media/"

CONTENT_DIR = base_dir_join("mediafiles/content")
PREVIEWS_DIR = base_dir_join("mediafiles/previews")
os.makedirs(CONTENT_DIR, exist_ok=True)
os.makedirs(PREVIEWS_DIR, exist_ok=True)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Speed up password hashing
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Celery
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False

CORS_ALLOWED_ORIGINS = []
CSRF_TRUSTED_ORIGINS = []

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-test",
    }
}

ALLOWED_FILE_MIME_TYPE = [
    "image/png",
    "image/jpeg",
    "text/plain",
    "application/pdf",
]
MAX_FILE_UPLOAD_MB = 50
