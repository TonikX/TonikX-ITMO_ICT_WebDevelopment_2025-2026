from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('owner/<int:owner_id>/', views.owner_detail, name='owner_detail'),
]