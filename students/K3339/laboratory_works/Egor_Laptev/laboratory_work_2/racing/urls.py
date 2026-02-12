from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import RaceListView

app_name = 'racing'

urlpatterns = [
    path('', RaceListView.as_view(), name="race_list"),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('race/<int:pk>/', views.race_detail, name='race_detail'),
    path('race/<int:race_pk>/register/', views.register_for_race, name='register'),
    path('registration/<int:reg_pk>/edit/', views.edit_registration, name='edit_registration'),
    path('registration/<int:reg_pk>/cancel/', views.cancel_registration, name='cancel_registration'),
    path('race/<int:race_pk>/comment/', views.add_comment, name='add_comment'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('car/add/', views.add_car, name='add_car'),
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='racing/login.html'), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register_user'),
]
