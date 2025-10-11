from django.urls import path
from . import views

urlpatterns = [
    path('owners/<int:car_owner_id>/', views.owner_list, name='owner_list'),
]