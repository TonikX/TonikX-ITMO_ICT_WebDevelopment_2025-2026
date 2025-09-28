from django.urls import path
from . import views
from .views import CarCreateView, CarDeleteView

urlpatterns = [
    path("cars/<int:car_id>/owners/", views.car_owners, name="car-owners"),
    path("cars/add/", CarCreateView.as_view(), name="car-add"),
    path("owners/", views.owner_list, name="owner-list"),
    path("owners/add/", views.add_owner, name="owner-add"),
    path('cars/<int:pk>/', views.CarDetailView.as_view(), name='car-detail'),
    path('cars/', views.CarListView.as_view(), name='car-list'),
    path('cars/<int:pk>/update/', views.CarUpdateView.as_view(), name='car-update'),
    path("cars/<int:pk>/delete/", CarDeleteView.as_view(), name="car-delete"),
]