from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('trips/', views.TripListView.as_view(), name='trip_list_last_month'),
    path('register/', views.register, name='register'),
    path('profile/', views.user_profile, name='user_profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/login.html'), name='logout'),
    path('trip/add/', views.add_trip, name='add_trip'),
    path('trip/<int:trip_id>/comment/', views.add_comment, name='add_comment'),
]