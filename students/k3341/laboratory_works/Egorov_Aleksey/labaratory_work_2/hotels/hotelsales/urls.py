from django.urls import path
from . import views

app_name = 'hotelsales'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('hotel/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    path('book/<int:room_type_id>/', views.booking_create, name='booking_create'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<int:booking_id>/review/', views.add_review, name='add_review'),
    path('booking/<int:booking_id>/edit/', views.edit_booking, name='edit_booking'),
    path('recent-guests/', views.recent_guests, name='recent_guests'),
]
