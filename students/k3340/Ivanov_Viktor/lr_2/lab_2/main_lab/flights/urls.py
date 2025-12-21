from django.urls import path
from . import views

urlpatterns = [
    # Главная страница
    path('', views.home, name='home'),
    
    # Аутентификация
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Рейсы
    path('flights/', views.FlightListView.as_view(), name='flight_list'),
    path('flights/<int:pk>/', views.FlightDetailView.as_view(), name='flight_detail'),
    
    # Резервирования
    path('flights/<int:flight_id>/reserve/', views.create_reservation, name='create_reservation'),
    path('my-reservations/', views.my_reservations, name='my_reservations'),
    path('reservations/<int:reservation_id>/cancel/', views.cancel_reservation, name='cancel_reservation'),
    
    # Отзывы
    path('flights/<int:flight_id>/review/', views.create_review, name='create_review'),
    path('my-reviews/', views.my_reviews, name='my_reviews'),
    path('reviews/<int:review_id>/delete/', views.delete_review, name='delete_review'),
]



