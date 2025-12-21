from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('owners/', owner_list, name='owner_list'),
    path("owner/<int:id>/", owner_detail, name="owner_detail"),
    path('owners/create/', owner_create, name='owner_create'),
    path('cars/', car_list, name='car_list'),
    path('add_car/', add_car, name='add_car'),
    path('cars/<int:id>/', car_detail, name='car_detail'),
    path('cars/<int:id>/update/', car_update, name='car_update'),
    path('cars/<int:id>/delete/', car_delete, name='car_delete'),
    path('ownership/', ownership_list, name='ownership_list'),
    path('ownership/<int:id>/', ownership_detail, name='ownership_detail'),
    path('add_ownership/', add_ownership, name='add_ownership'),
]
