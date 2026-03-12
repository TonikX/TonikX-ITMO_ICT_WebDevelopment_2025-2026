from django.urls import path
from . import views

urlpatterns = [
    path('', views.hotel_list, name='hotels_list'),
    path('hotel/<int:pk>/', views.hotel_detail, name='hotel_detail'),
    path('rooms/', views.RoomListView.as_view(), name='rooms_list'),
    path('room/<int:pk>/', views.room_detail, name='room_detail'),

    path('reserve/', views.create_reservation, name='create_reservation'),
    path('my_reservations/', views.my_reservations, name='my_reservations'),

    path('reservation/<int:pk>/checkin/', views.reservation_checkin, name='reservation_checkin'),
    path('reservation/<int:pk>/checkout/', views.reservation_checkout, name='reservation_checkout'),
    path('reservation/<int:pk>/edit/', views.edit_reservation, name='edit_reservation'),
    path('reservation/<int:pk>/cancel/', views.cancel_reservation, name='cancel_reservation'),
    path('reservation/<int:pk>/review/', views.reservation_review, name='reservation_review'),

    path('room/<int:room_pk>/review/', views.add_review, name='add_review'),

    path('guests_last_month/', views.guests_last_month, name='guests_last_month'),
    path('register/', views.register, name='register'),

]
