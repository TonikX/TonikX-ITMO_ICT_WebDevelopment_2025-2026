from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.TourListView.as_view(), name='tour_list'),
    path('reserve/<int:tour_id>/', views.reserve_tour, name='reserve_tour'),
    path('change/<int:tour_id>/<int:reservation_id>/', views.change_tour, name='change_tour'),
    path('my-reservations/', views.my_reservations, name='my_reservations'),
    path('delete-reservation/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),
    path('review/<int:tour_id>/', views.add_review, name='add_review'),
    path('sold-tours/', views.sold_tours_by_country, name='sold_tours'),
    path('tour/<int:tour_id>/reviews/', views.tour_reviews, name='tour_reviews')
]