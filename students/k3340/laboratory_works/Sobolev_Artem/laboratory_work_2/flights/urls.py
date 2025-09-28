from django.urls import path
from .views import (
    FlightListView, FlightDetailView,
    ReservationCreateView, ReservationUpdateView, ReservationDeleteView, ReviewCreateView, SignUpView, FlightUpdateView,
    FlightDeleteView, FlightStatusUpdateView, ReviewDeleteView,
)

app_name = "flights"

urlpatterns = [
    path("flights/", FlightListView.as_view(), name="flight-list"),
    path("flights/<int:pk>/", FlightDetailView.as_view(), name="flight-detail"),
    path("flights/<int:flight_pk>/reserve/", ReservationCreateView.as_view(), name="reservation-create"),
    path("reservations/<int:pk>/edit/", ReservationUpdateView.as_view(), name="reservation-update"),
    path("reservations/<int:pk>/delete/", ReservationDeleteView.as_view(), name="reservation-delete"),
    path("flights/<int:flight_pk>/reviews/new/", ReviewCreateView.as_view(), name="review-create"),
    path("flights/<int:pk>/update/", FlightUpdateView.as_view(), name="flight-update"),
    path("flights/<int:pk>/delete/", FlightDeleteView.as_view(), name="flight-delete"),
    path('flights/<int:pk>/status-update/', FlightStatusUpdateView.as_view(), name='flight-status-update'),
    path("accounts/signup/", SignUpView.as_view(), name="signup"),
    path('reviews/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
]
