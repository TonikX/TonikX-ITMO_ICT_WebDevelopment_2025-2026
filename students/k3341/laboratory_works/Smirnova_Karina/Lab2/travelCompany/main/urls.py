from django.urls import path
from . import views

urlpatterns = [
    path('tours/', views.tour_list, name='tour_list'),
    path('tours/<int:pk>/', views.tour_detail, name='tour_detail'),
    path('tours/<int:pk>/reserve/', views.reserve_tour, name='reserve_tour'),
    path('tours/<int:pk>/cancel/', views.cancel_reservation, name='cancel_reservation'),
    path('tours/create/', views.create_tour, name='create_tour'),
    path('tours/<int:pk>/edit/', views.edit_tour, name='edit_tour'),
    path('tours/<int:pk>/delete/', views.delete_tour, name='delete_tour'),
    path('admin/reservations/', views.reservations_admin, name='reservations_admin'),
    path('admin/reservations/<int:pk>/approve/', views.approve_reservation, name='approve_reservation'),
    path('admin/reservations/<int:pk>/decline/', views.refuse_reservation, name='decline_reservation'),
]