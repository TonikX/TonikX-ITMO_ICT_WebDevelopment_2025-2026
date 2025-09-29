from django.urls import path
from . import views

urlpatterns = [
    path('', views.flight_list, name='flight_list'),
    path('flight/<int:flight_id>/', views.flight_detail, name='flight_detail'),
    path('flight/<int:flight_id>/reserve/', views.make_reservation, name='make_reservation'),
    path('reservation/<int:reservation_id>/edit/', views.edit_reservation, name='edit_reservation'),
    path('reservation/<int:reservation_id>/cancel/', views.cancel_reservation, name='cancel_reservation'),
    path('flight/<int:flight_id>/review/', views.add_review, name='add_review'),
    path('register/', views.register, name='register'),
    path('my-reservations/', views.user_reservations, name='user_reservations'),
]
