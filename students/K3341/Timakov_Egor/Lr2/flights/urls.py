from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.FlightListView.as_view(), name='flight_list'),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='flights/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('flight/<int:pk>/', views.flight_detail, name='flight_detail'),
    path('flight/<int:flight_id>/reserve/', views.create_reservation, name='create_reservation'),
    path('flight/<int:flight_id>/review/', views.create_review, name='create_review'),
    path('flight/<int:flight_id>/passengers/', views.flight_passengers, name='flight_passengers'),
    path('reservations/', views.my_reservations, name='my_reservations'),
    path('reservation/<int:reservation_id>/edit/', views.edit_reservation, name='edit_reservation'),
    path('reservation/<int:reservation_id>/delete/', views.delete_reservation, name='delete_reservation'),
]



