# vehicles/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('owners/', views.user_list, name='user_list'),
    path('owners/create/', views.register_user, name='register_user'),
    path('owners/<int:user_id>/', views.user_detail, name='user_detail'),

    # Автомобили — классовые представления
    path('cars/', views.CarListView.as_view(), name='car_list'),
    path('cars/<int:pk>/', views.CarDetailView.as_view(), name='car_detail'),
    path('cars/create/', views.CarCreateView.as_view(), name='car_create'),
    path('cars/<int:pk>/update/', views.CarUpdateView.as_view(), name='car_update'),
    path('cars/<int:pk>/delete/', views.CarDeleteView.as_view(), name='car_delete'),
]