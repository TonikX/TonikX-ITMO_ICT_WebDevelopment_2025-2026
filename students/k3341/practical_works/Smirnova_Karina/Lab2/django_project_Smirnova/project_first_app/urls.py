from django.urls import path
from . import views
from .views import CarListView, CarDetailView, CarCreateView, CarUpdateView, CarDeleteView

urlpatterns = [
    path('owner/<int:owner_id>/', views.owner_detail, name='owner_detail'),
    path('owners/', views.owner_list, name='owner_list'),
    path('cars/', CarListView.as_view(), name='car_list'),
    path('cars/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('owners/create/', views.owner_create_view, name='owner_create'),
    path('cars/create/', CarCreateView.as_view(), name='car_create'),
    path('cars/<int:pk>/update/', CarUpdateView.as_view(), name='car_update'),
    path('cars/<int:pk>/delete/', CarDeleteView.as_view(), name='car_delete'),
]