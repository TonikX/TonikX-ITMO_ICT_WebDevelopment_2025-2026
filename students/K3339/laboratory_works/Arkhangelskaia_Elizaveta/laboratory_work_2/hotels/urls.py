from django.urls import path
from .views import register, hotels, all_rooms, book_room, room_info, home
from django.contrib import admin
urlpatterns = [
    path('register/', register, name='register'),
    path('hotels/', hotels, name='hotels'),
    path('all_rooms/', all_rooms, name='all_rooms'),
    path('book_room/<int:pk>', book_room, name='book_room'),
    path('room_info/<int:pk>', room_info, name='room_info'),
    path('', home, name='home')
]

