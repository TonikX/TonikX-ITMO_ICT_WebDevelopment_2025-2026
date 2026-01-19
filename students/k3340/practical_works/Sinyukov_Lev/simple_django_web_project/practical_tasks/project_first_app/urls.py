from django.urls import path
from .views import (
    owners_list, owner_detail, owner_create,
    CarListView, CarDetailView, CarCreateView, CarUpdateView, CarDeleteView
)

urlpatterns = [
    path('owners/', owners_list, name='owners_list'),
    path('owner/create/', owner_create, name='owner_create'),
    path('owner/<int:owner_id>/', owner_detail, name='owner_detail'),

    path('cars/', CarListView.as_view(), name='car-list'),
    path('cars/create/', CarCreateView.as_view(), name='car-create'),
    path('cars/<int:pk>/', CarDetailView.as_view(), name='car-detail'),
    path('cars/<int:pk>/update/', CarUpdateView.as_view(), name='car-update'),
    path('cars/<int:pk>/delete/', CarDeleteView.as_view(), name='car-delete')
]