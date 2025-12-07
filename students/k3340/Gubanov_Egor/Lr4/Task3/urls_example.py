from django.urls import path
from .views import test_cors

urlpatterns = [
    path('test-cors/', test_cors, name='test-cors'),
]

