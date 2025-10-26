from django.urls import path, include
from . import views

urlpatterns = [
    path('mark/top/', views.mark_top, name='mark_top'),
    path('mark/all/', views.mark_all, name='mark_all'),
    path('routes/pick/', views.routes_pick, name='routes_pick'),
    path('flights/<int:id>/available_seats/', views.flights_available_seats, name='flights_available_seats'),
    path('planes/in_repair/', views.planes_in_repair, name='planes_in_repair'),
    path('employees/count/', views.employees_count, name='employees_count'),
]