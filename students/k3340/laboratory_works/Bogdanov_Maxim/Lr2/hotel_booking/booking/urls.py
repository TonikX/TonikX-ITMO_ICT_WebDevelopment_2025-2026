from django.urls import path
from . import views

urlpatterns = [
    path('', views.HotelListView.as_view(), name='hotel_list'),
    path('hotels/<int:pk>/', views.HotelDetailView.as_view(), name='hotel_detail'),
    path('hotels/<int:hotel_id>/rooms/', views.RoomListView.as_view(), name='hotel_rooms'),

    path('bookings/new/', views.BookingCreateView.as_view(), name='booking_create'),
    path('bookings/my/', views.MyBookingsView.as_view(), name='my_bookings'),
    path('bookings/<int:pk>/', views.BookingDetailView.as_view(), name='booking_detail'),
    path('bookings/<int:pk>/edit/', views.BookingUpdateView.as_view(), name='booking_update'),
    path('bookings/<int:pk>/delete/', views.BookingDeleteView.as_view(), name='booking_delete'),

    path('reviews/new/<int:booking_id>/', views.ReviewCreateView.as_view(), name='review_create'),
    path('reviews/my/', views.MyReviewsView.as_view(), name='my_reviews'),
    path('reviews/<int:pk>/edit/', views.ReviewUpdateView.as_view(), name='review_update'),
    path('reviews/<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='review_delete'),
]