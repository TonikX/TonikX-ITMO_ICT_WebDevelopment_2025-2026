from django.urls import path
from . import views

urlpatterns = [
    path('owner/<int:owner_id>/', views.owner_detail, name='owner_detail'),
]
