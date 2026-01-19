from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # Маршруты для аутентификации
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('accounts/', include('django.contrib.auth.urls')),
    # Маршруты для владельцев (функциональные представления)
    path('owners/', views.owners_list, name='owners_list'),
    path('owner/<int:owner_id>/', views.owner_detail, name='owner_detail'),
    path('owner/create/', views.owner_create, name='owner_create'),
    path('owner/<int:owner_id>/update/', views.owner_update, name='owner_update'),
    path('owner/<int:owner_id>/delete/', views.owner_delete, name='owner_delete'),
    # Маршруты для автомобилей (классовые представления)
    path('cars/', views.CarListView.as_view(), name='car_list'), 
    path('cars/<int:pk>/', views.CarDetailView.as_view(), name='car_detail'),
    path('cars/create/', views.CarCreateView.as_view(), name='car_create'),
    path('cars/<int:pk>/update/', views.CarUpdateView.as_view(), name='car_update'),
    path('cars/<int:pk>/delete/', views.CarDeleteView.as_view(), name='car_delete'),
]
