from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.tour_list, name='tour_list'),
    path('tour/<int:pk>/', views.tour_detail, name='tour_detail'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='tours/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('tour/<int:pk>/reserve/', views.reserve_tour, name='reserve_tour'),
    path('my-reservations/', views.my_reservations, name='my_reservations'),
    path('reservation/<int:pk>/edit/', views.edit_reservation, name='edit_reservation'),
    path('reservation/<int:pk>/delete/', views.delete_reservation, name='delete_reservation'),
    path('tour/<int:pk>/review/', views.add_review, name='add_review'),
    path('sales/', views.sales_by_country, name='sales_by_country'),
]
