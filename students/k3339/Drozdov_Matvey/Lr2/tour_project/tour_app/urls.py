from django.urls import path
from . import views

urlpatterns = [
    path('', views.tour_list, name='tour_list'),
    path("register/", views.register, name="register"),
    path('tours/<int:pk>/', views.tour_detail, name='tour_detail'),
    path('tours/<int:pk>/review/', views.add_review, name='add_review'),
    path('tours/<int:pk>/book/', views.book_tour, name='book_tour'),
    path('my-reservations/', views.my_reservations, name='my_reservations'),
    path('reservations/<int:pk>/cancel/', views.cancel_reservation, name='cancel_reservation'),
    path('stats/sales-by-country/', views.sales_by_country, name='sales_by_country')
]
