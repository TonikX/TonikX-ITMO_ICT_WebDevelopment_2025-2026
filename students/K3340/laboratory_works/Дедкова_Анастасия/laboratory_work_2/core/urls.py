from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.FlightListView.as_view(), name='flight_list'),
    path('flights/<int:flight_id>/', views.FlightDetailView.as_view(), name='flight_detail'),
    path('flights/<int:flight_id>/book/', views.create_booking, name='booking_create'),

    path('bookings/', views.MyBookingListView.as_view(), name='my_bookings'),
    path('bookings/<int:pk>/delete/', views.BookingDeleteView.as_view(), name='booking_delete'),

    path('flights/<int:flight_id>/passengers/', views.flight_passengers, name='flight_passengers'),
    path('flights/<int:flight_id>/passengers/add/', views.flight_add_passenger, name='flight_add_passenger'),
    path('flights/<int:flight_id>/passengers/<int:booking_id>/delete/', views.flight_delete_passenger,
         name='flight_delete_passenger'),
    path('flights/<int:pk>/review/', views.create_review, name='review_create'),
    path('signup/', views.signup, name='signup'),
    path('bookings-list/', views.bookings_list, name='bookings_list'),
    path('flights/<int:flight_id>/reviews/<int:pk>/delete/',
         views.review_delete,
         name='review_delete'),
]
