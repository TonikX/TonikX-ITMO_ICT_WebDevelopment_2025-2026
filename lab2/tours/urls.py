from django.urls import path
from . import views

urlpatterns = [
    path('', views.tour_list, name='tour_list'),
    path('tour/<int:pk>/', views.tour_detail, name='tour_detail'),
    path('tour/<int:tour_id>/reserve/', views.create_reservation, name='create_reservation'),
    path('tour/<int:tour_id>/review/', views.create_review, name='create_review'),
    path('my-reservations/', views.my_reservations, name='my_reservations'),
    path('reservation/<int:pk>/edit/', views.edit_reservation, name='edit_reservation'),
    path('reservation/<int:pk>/delete/', views.delete_reservation, name='delete_reservation'),
    path('sold-tours/', views.sold_tours_by_country, name='sold_tours_by_country'),
    path('register/', views.register, name='register'),
]

