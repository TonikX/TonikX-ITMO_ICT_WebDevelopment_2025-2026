from django.contrib.auth.views import LogoutView
from django.urls import path

from tourProject import settings
from . import views
from .views import TourReviewsView

urlpatterns = [
    path('agencies/', views.AgencyListView.as_view(), name='agencies'),
    path('agencies/<int:agency_id>/tours/', views.agency_tours, name='agency_tours'),
    path('tours/', views.TourListView.as_view(), name='tours'),
    path('tours/<int:tour_id>/reserve/', views.create_reservation, name='reserve_tour'),
    path('tours/<int:tour_id>/reviews/', TourReviewsView.as_view(), name='tour_reviews'),
    path('tours/<int:tour_id>/reviews/create/', views.create_review, name='create_review'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('reservations/', views.user_reservations, name='reservations'),
    path('reservations/<int:pk>/delete/', views.ReservationDeleteView, name='reservation_delete'),
    path('pending-reservations/', views.pending_reservations, name='pending_reservations'),
    path('update-reservation-status/<int:pk>/<str:new_status>/', views.update_reservation_status,
         name='update_reservation_status'),
    path('sold-tours/', views.sold_tours_by_country, name='sold_tours_by_country'),
]
