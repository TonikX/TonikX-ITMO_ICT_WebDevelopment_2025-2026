from django.urls import path
from . import views
from .views import SignUpView

urlpatterns = [
    path('', views.hotels_list, name='hotels_list'),
    path('hotel/<int:pk>/', views.hotel_detail, name='hotel_detail'),
    path('room/<int:room_id>/reserve/', views.reserve_room, name='reserve_room'),
    path('my_reservations/', views.my_reservations, name='my_reservations'),
    path('reservation/<int:pk>/cancel/', views.cancel_reservation, name='cancel_reservation'),
    path('reservation/<int:pk>/edit/', views.edit_reservation, name='edit_reservation'),
    path('room/<int:room_id>/review/', views.write_review, name='write_review'),
    path('occupants/', views.occupants_last_month, name='occupants'),
    path('signup/', SignUpView.as_view(), name='signup'),
]

