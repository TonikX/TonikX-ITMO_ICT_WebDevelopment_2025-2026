from django.urls import path
from . import views

urlpatterns = [
    path('', views.flight_list, name='flight_list'),
    path('flight/<int:pk>/', views.flight_detail, name='flight_detail'),
    path('flight/<int:flight_id>/reserve/', views.make_reservation, name='make_reservation'),
    path('flight/<int:flight_id>/passengers/', views.passengers_list, name='passengers_list'),
    path('flight/<int:flight_id>/review/', views.add_review, name='add_review'),
    path('reservations/', views.my_reservations, name='my_reservations'),
    path('reservation/<int:pk>/edit/', views.edit_reservation, name='edit_reservation'),
    path('reservation/<int:pk>/delete/', views.delete_reservation, name='delete_reservation'),
    path('reservation/<int:reservation_id>/register-passenger/', views.register_passenger, name='register_passenger'),
    path('register/', views.register, name='register'),
]
