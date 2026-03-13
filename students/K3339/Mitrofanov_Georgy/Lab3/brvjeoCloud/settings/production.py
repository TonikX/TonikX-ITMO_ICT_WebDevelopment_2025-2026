import re

from .base import *


DEBUG = True

SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(",")

CORS_ALLOWED_ORIGIN_REGEXES = [
    re.compile(r) for r in env("CORS_ALLOWED_ORIGIN_REGEXES", "").split(",") if r
]
CSRF_TRUSTED_ORIGINS = env("CSRF_TRUSTED_ORIGINS", "").split(",")

DATABASES["default"]["ATOMIC_REQUESTS"] = True

STATIC_URL = "static/"
STATIC_ROOT = base_dir_join("staticfiles")

MEDIA_ROOT = base_dir_join("mediafiles/")
MEDIA_URL = "/media/"

CONTENT_DIR = base_dir_join("mediafiles/content")
PREVIEWS_DIR = base_dir_join("mediafiles/previews")
os.makedirs(CONTENT_DIR, exist_ok=True)
os.makedirs(PREVIEWS_DIR, exist_ok=True)

# Celery
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="")
CELERY_RESULT_BACKEND = env("REDIS_URL")
CELERY_SEND_TASK_ERROR_EMAILS = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "logging.Formatter",
            "fmt": "%(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
    },
    "loggers": {
        "json": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.server": {
            "handlers": [],  
            "level": "ERROR",
            "propagate": False,
        },
    },
}

import logging.config


logging.config.dictConfig(LOGGING)

MAX_FILE_UPLOAD_MB = 50
ALLOWED_FILE_MIME_TYPE = [
    "image/jpeg",
    "image/png",
    "video/mp4",
    "application/pdf",
]