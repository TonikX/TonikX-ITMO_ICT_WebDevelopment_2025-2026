from django.urls import path
from . import views

urlpatterns = [
    path('owners/<int:car_id>/', views.owner_list, name='owner_list'),
    path('cars/', views.CarListView.as_view(), name='car_list'),
    path('cars/<int:pk>/', views.CarDetailView.as_view(), name='car_detail'),
    path('cars/<int:pk>/edit/', views.CarUpdateView.as_view(), name='car_update'),
    path('cars/<int:car_id>/add_owner/', views.add_owner_to_car, name='add_owner_to_car'),
    path('cars/<int:pk>/delete/', views.CarDeleteView.as_view(), name='car_delete'),
    path('cars/add/', views.CarCreateView.as_view(), name='car_add'),
]