from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.hotel_list, name='hotel_list'),
    path('hotel/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    path('hotel/<int:hotel_id>/recent_guests/', views.recent_guests, name='recent_guests'),
    path('owner/<int:owner_id>/', views.owner_detail, name='owner_detail'),
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('reservations/new/', views.make_reservation, name='make_reservation'),
    path('reservations/<int:reservation_id>/edit/', views.edit_reservation, name='edit_reservation'),
    path('reservations/<int:reservation_id>/delete/', views.delete_reservation, name='delete_reservation'),
    path('reviews/', views.review_list, name='review_list'),
    path('reviews/new/', views.add_review, name='add_review'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
