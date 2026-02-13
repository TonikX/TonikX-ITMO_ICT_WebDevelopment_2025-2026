from operator import index

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from hwboard.views import *

urlpatterns = [
    path('', base, name='main'),
    path('admin/', admin.site.urls),
    path('', include('hwboard.urls')),
]


handler404 = pageNotFound