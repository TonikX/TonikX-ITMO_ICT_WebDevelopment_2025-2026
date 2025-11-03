from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.flight_list, name='flight_list'),
    path('flights/<int:flight_id>/', views.flight_detail, name='flight_detail'),
    path('flights/<int:flight_id>/reserve/', views.create_reservation, name='create_reservation'),
    path('flights/<int:flight_id>/comment/', views.add_comment, name='add_comment'),

    path('reservations/<int:pk>/edit/', views.reservation_update, name='reservation_update'),
    path('reservations/<int:pk>/delete/', views.reservation_delete, name='reservation_delete'),
    path('my/reservations/', views.my_reservations, name='my_reservations'),

    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
]
