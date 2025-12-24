from django.urls import path
from . import views

urlpatterns = [
    path('owners/', views.owner_list, name='owner_list'),
    path('owner/<int:owner_id>/', views.owner_detail, name='owner_detail'),
    path('owner/create/', views.owner_create, name='owner_create'),

    path('cars/', views.CarListView.as_view(), name='car_list'),
    path('car/<int:pk>/', views.CarDetailView.as_view(), name='car_detail'),
    path('car/<int:pk>/update/', views.CarUpdateView.as_view(), name='car_update'),
    path('car/create/', views.CarCreateView.as_view(), name='car_create'),
    path('car/<int:pk>/update/', views.CarUpdateView.as_view(), name='car_update'),
    path('car/<int:pk>/delete/', views.CarDeleteView.as_view(), name='car_delete'),

    path('time/', views.current_time, name='current_time'),
    path('health/', views.health_check, name='health_check'),
]