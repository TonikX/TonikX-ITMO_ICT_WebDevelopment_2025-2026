from django.urls import path
from .reports import quarter_report

urlpatterns = [
    path("quarter/", quarter_report),
]