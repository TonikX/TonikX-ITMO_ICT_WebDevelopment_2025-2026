from django.urls import path
from . import views


urlpatterns = [
    path('', views.flight_list, name='flight_list'),
    path('register/', views.register, name='register'),
    path('flight/<int:flight_id>', views.flight_detail, name='flight_detail'),
    path('flight/<int:flight_id>/reserve/', views.create_reservation, name='create_reservation'),
    path('flight/<int:flight_id>/comment/', views.add_comment, name='add_comment'),
]
