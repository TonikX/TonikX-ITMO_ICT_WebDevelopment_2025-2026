# automobiles/urls.py

from django.urls import path
from . import views
from .views import CarListView, CarDetailView, CarUpdateView, CarCreateView, CarDeleteView

urlpatterns = [
    # Главная страница
    path('', views.home, name='automobiles_home'),

    # Владельцы (функциональные представления)
    path('owners/', views.owners_list, name='owners_list'),
    path('owner/<int:owner_id>/', views.owner_detail, name='owner_detail'),
    path('owner/create/', views.owner_create, name='owner_create'),
    path('owner/<int:owner_id>/update/', views.owner_update, name='owner_update'),
    path('owner/<int:owner_id>/delete/', views.owner_delete, name='owner_delete'),
    path('owner/<int:owner_id>/add-license/', views.add_license, name='add_license'),

    # Автомобили (классовые представления)
    path('cars/', CarListView.as_view(), name='cars_list_class'),
    path('car/<int:pk>/', CarDetailView.as_view(), name='car_detail_class'),
    path('car/<int:pk>/update/', CarUpdateView.as_view(), name='car_update'),
    path('car/create/', CarCreateView.as_view(), name='car_create'),
    path('car/<int:pk>/delete/', CarDeleteView.as_view(), name='car_delete'),

    # Старые URL для обратной совместимости
    path('cars-old/', views.cars_list, name='cars_list'),
    path('car-old/<int:car_id>/', views.car_detail, name='car_detail'),
]