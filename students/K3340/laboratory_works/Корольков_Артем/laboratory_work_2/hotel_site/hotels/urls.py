from django.urls import path
from .views import (
    HotelListView,
    ReservationCreateView,
    UserReservationListView,
    ReservationUpdateView,
    ReservationDeleteView,
    ReviewCreateView,
    ReviewListView,
    UserReviewListView,
    ReviewDeleteView,
    guest_report,
    AllReservationsListView,
    user_login, user_logout, profile, register

)

urlpatterns = [
    path('', HotelListView.as_view(), name='hotel_list'),

    # Бронирования
    path('reservations/', UserReservationListView.as_view(), name='user_reservations'),
    path('reservations/new/', ReservationCreateView.as_view(), name='create_reservation'),
    path('reservations/<int:pk>/edit/', ReservationUpdateView.as_view(), name='update_reservation'),
    path('reservations/<int:pk>/delete/', ReservationDeleteView.as_view(), name='delete_reservation'),
    path('reservations/all/', AllReservationsListView.as_view(), name='all_reservations'),

    # Отзывы
    path('reviews/', ReviewListView.as_view(), name='review_list'),
    path('reviews/my/', UserReviewListView.as_view(), name='user_reviews'),
    path('reviews/new/', ReviewCreateView.as_view(), name='create_review'),
    path('reviews/<int:pk>/delete/', ReviewDeleteView.as_view(), name='delete_review'),

    # Отчет
    path('report/', guest_report, name='guest_report'),

    # Аутентификация
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('register/', register, name='register'),
]