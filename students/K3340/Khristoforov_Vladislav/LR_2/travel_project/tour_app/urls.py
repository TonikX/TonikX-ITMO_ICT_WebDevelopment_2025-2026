from django.urls import path
from .views import (
    TourListView, TourDetailView, MyBookingsListView, 
    edit_booking, delete_booking, statistics,
    confirm_booking, cancel_booking_admin, delete_review, 
    add_tour, management_dashboard
)

urlpatterns = [
    path('', TourListView.as_view(), name='tour_list'),
    path('tour/<int:pk>/', TourDetailView.as_view(), name='tour_detail'),
    path('my-bookings/', MyBookingsListView.as_view(), name='my_bookings'),
    path('booking/<int:booking_id>/edit/', edit_booking, name='edit_booking'),
    path('booking/<int:booking_id>/delete/', delete_booking, name='delete_booking'),
    path('booking/<int:booking_id>/confirm/', confirm_booking, name='confirm_booking'),
    path('booking/<int:booking_id>/cancel-admin/', cancel_booking_admin, name='cancel_booking_admin'),
    path('statistics/', statistics, name='statistics'),
    path('management/', management_dashboard, name='management_dashboard'),
    path('review/<int:review_id>/delete/', delete_review, name='delete_review'),
    path('add-tour/', add_tour, name='add_tour'),
]