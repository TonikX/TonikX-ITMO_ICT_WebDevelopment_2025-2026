import os
import sys

from celery import Celery


settings_module = os.environ.get("DJANGO_SETTINGS_MODULE", default=None)
if settings_module is None:
    print(
        "Error: no DJANGO_SETTINGS_MODULE found. Will NOT start devserver. "
        "Remember to create .env file at project root. "
        "Check README for more info."
    )
    sys.exit(1)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

app = Celery("brvjeoCloud_tasks")  # type: ignore
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
