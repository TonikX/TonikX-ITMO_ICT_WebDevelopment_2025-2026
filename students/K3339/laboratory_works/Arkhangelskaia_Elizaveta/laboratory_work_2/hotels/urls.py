from django.urls import path
from .views import register, hotels, all_rooms, book_room, room_info, home, reservations
from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', register, name='register'),
    path('hotels/', hotels, name='hotels'),
    path('all_rooms/', all_rooms, name='all_rooms'),
    path('book_room/<int:pk>', book_room, name='book_room'),
    path('room_info/<int:pk>', room_info, name='room_info'),
    path('', home, name='home'),
    path('reservations/', reservations, name='reservations'),
    path('reservation/<int:pk>/edit/', views.ReservationUpdateView.as_view(), name='edit_reservation'),
    path('reservation/<int:pk>/delete/', views.ReservationDeleteView.as_view(), name='delete_reservation'),
    path('guests/', views.last_month_guests, name='last_month_guests'),
]

