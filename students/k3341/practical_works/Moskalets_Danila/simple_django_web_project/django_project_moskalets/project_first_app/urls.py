from django.urls import path

from .views import *

urlpatterns = [
    path('owners/', owners_list,  name='owners_list_url'),
    path('owner/<int:owner_id>/', owner_detail, name='owner_detail'),
    path('owners/create/', owners_create, name='owners_create'),
    path('cars/', CarsListView.as_view(), name='cars_list_url'),
    path('cars/create', CarsCreateView.as_view(), name='cars_create_url'),
    path('car/<int:pk>/update/', CarUpdateView.as_view(), name='car_update_url'),
    path('car/<int:pk>/delete/', CarDeleteView.as_view(), name='car_delete_url'),
    path('car/<int:pk>/', CarsDetailView.as_view(), name='car_detail'),
    path('ownership/create/', OwnershipCreateView.as_view(), name='ownership_create'),
    path('user/create/', CarUserCreateView.as_view(), name='caruser_create'),

]
