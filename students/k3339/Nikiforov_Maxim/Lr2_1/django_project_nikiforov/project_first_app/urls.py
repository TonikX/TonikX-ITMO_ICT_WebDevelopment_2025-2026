from django.urls import path
from . import views

urlpatterns = [
    # Владельцы (функциональные представления)
    path('owner/list/', views.owner_list, name='owner_list'),
    path('owner/create/', views.create_owner, name='owner_create'),
    path('owner/<int:owner_id>/', views.owner_detail, name='owner_detail'),
    
    # Автомобили (представления на основе классов)
    path('car/list/', views.CarListView.as_view(), name='car_list'),
    path('car/create/', views.CarCreateView.as_view(), name='car_create'),
    path('car/<int:car_id>/', views.CarDetailView.as_view(), name='car_detail'),
    path('car/<int:car_id>/update/', views.CarUpdateView.as_view(), name='car_update'),
    path('car/<int:car_id>/delete/', views.CarDeleteView.as_view(), name='car_delete'),
]

