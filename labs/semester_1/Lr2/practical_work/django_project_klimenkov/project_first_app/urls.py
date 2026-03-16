from django.urls import path
from . import views


urlpatterns = [
    path('', views.root_redirect),

    # Владельцы
    path('owner/list/', views.owners_list, name='owners_list'),
    path('owner/<int:id>/', views.owner_detail, name='owner_detail'),
    path('owner/create/', views.create_owner, name='create_owner'),
    path('owner/edit/<int:id>/', views.edit_owner, name='edit_owner'),
    path('owner/delete/<int:id>/', views.delete_owner, name='delete_owner'),

    # Автомобили
    path('car/list/', views.CarsListView.as_view(), name='cars_list'),
    path('car/<int:car_id>/', views.CarDetailView.as_view(), name='car_detail'),
    path('car/create/', views.CarCreateView.as_view(), name='create_car'),
    path('car/edit/<int:car_id>/', views.CarUpdateView.as_view(), name='edit_car'),
    path('car/delete/<int:car_id>/', views.CarDeleteView.as_view(), name='delete_car'),
]
