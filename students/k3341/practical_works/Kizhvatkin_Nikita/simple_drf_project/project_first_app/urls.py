from django.urls import path
from . import views

urlpatterns = [
    # owners
    path('owners/', views.owner_list, name='owner_list'),
    path('owners/<int:owner_id>/', views.owner_detail, name='owner_detail'),
    # cars
    path('cars/', views.CarListView.as_view(), name='car_list'),
    path('car/<int:pk>/', views.CarDetailView.as_view(), name='car_detail'),
    path('car/<int:pk>/delete/', views.CarDeleteView.as_view(), name='car_delete'),
]
