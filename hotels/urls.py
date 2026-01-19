from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('hotel/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    path('room/<int:room_id>/', views.room_detail, name='room_detail'),
    path('room/<int:room_id>/reserve/', views.create_reservation, name='create_reservation'),
    path('reservations/', views.my_reservations, name='my_reservations'),
    path('reservation/<int:reservation_id>/edit/', views.edit_reservation, name='edit_reservation'),
    path('reservation/<int:reservation_id>/delete/', views.delete_reservation, name='delete_reservation'),
    path('room/<int:room_id>/review/', views.add_review, name='add_review'),
    path('guests/', views.recent_guests, name='recent_guests'),
]
