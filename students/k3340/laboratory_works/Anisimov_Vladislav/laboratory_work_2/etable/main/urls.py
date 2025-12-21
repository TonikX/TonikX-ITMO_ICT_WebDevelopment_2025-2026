from django.urls import path
from .views import *

urlpatterns = [
    path('', table, name='table'),
    path('upload/', upload, name='upload'),
    path('grades/', grades, name='grades'),
]
