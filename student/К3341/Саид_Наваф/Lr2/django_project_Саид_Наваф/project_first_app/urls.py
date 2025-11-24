from django.urls import path , include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    
    # Racer URLs
    path('racers/', views.racer_list, name='racer_list'),
    path('racers/<int:racer_id>/', views.racer_detail, name='racer_detail'),
    path('racers/register/', views.register_user, name='register_user'),
    
    # Race URLs
    path('races/', views.RaceListView.as_view(), name='race_list'),
    path('races/<int:pk>/', views.RaceDetailView.as_view(), name='race_detail'),
    path('races/<int:race_id>/register/', views.race_register, name='race_register'),
    path('races/registration/<int:registration_id>/delete/', views.race_unregister, name='race_unregister'),
    path('races/<int:race_id>/comment/', views.add_race_comment, name='add_race_comment'),
    path('results/', views.race_results, name='race_results'),
    
    # Car URLs (FIXED - remove typos)
    path('cars/', views.CarListView.as_view(), name='car_list'),
    path('cars/<int:pk>/', views.CarDetailView.as_view(), name='car_detail'),
    path('cars/create/', views.CarCreateView.as_view(), name='car_create'),
    path('cars/<int:pk>/update/', views.CarUpdateView.as_view(), name='car_update'),
    path('cars/<int:pk>/delete/', views.CarDeleteView.as_view(), name='car_delete'),
    
    # Team URLs
    path('teams/', views.TeamListView.as_view(), name='team_list'),
    path('teams/<int:pk>/', views.TeamDetailView.as_view(), name='team_detail'),
       # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='project_first_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    
    # Search URL
    path('search/', views.search, name='search'),
]