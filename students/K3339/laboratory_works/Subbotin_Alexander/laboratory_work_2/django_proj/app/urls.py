from django.urls import path, include
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    # About page on root
    path('', TemplateView.as_view(template_name='about.html'), name='about'),
    # Tours list
    path('tour/', views.TourListView.as_view(), name='tour_list'),
    path('tour/<int:pk>/', views.TourDetailView.as_view(), name='tour_detail'),
    
    # autorithation
    path('accounts/', include('django.contrib.auth.urls')),
    path("register/", views.register, name="register"),
    path("profile/", views.ProfileUpdateView.as_view(), name="profile"),


    path('tour/add/', views.TourCreateView.as_view(), name='tour_create'),
    
    # Terms and Conditions static page
    path('terms/', TemplateView.as_view(template_name='terms_and_conditions.html'), name='terms'),
    # Reservation: quick book (one button) and manage
    path('reservation/add/<int:tour_id>/', views.ReservationCreateView, name='reservation_add'),
    path('reservation/', views.UserReservationListView.as_view(), name='user_reservations'),
    path('reservation/<int:pk>/delete/', views.ReservationDeleteView.as_view(), name='reservation_delete'),


    # Sold tours by city
    path('sold-by-city/', views.SoldByCityView.as_view(), name='sold_by_city'),
]