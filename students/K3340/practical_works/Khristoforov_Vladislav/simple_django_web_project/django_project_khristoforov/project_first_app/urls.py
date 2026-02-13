from django.urls import path 
from . import views 

urlpatterns = [
    path('user/', views.user_list, name='user_list'),
    path('user/<int:user_id>/', views.user_detail, name='user_detail'),
    path('user/create/', views.create_user, name='create_user'),

    path('car/', views.CarListView.as_view(), name='car_list'),
    path('car/create', views.CarCreateView.as_view(), name='car_create'),
    path('car/<int:pk>/', views.CarDetailView.as_view(), name='car_detail'),
    path('car/<int:pk>/update/', views.CarUpdateView.as_view(), name='car_update'),
    path('cars/<int:pk>/delete/', views.CarDeleteView.as_view(), name='car_delete'),
]