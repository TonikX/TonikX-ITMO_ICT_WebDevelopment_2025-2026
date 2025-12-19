from django.urls import path
from django.contrib.auth import views as auth_views

from winners import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.base_register, name='base_register'),
    path('login/', auth_views.LoginView.as_view(template_name='winners/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('choose-role/', views.choose_role, name='choose_role'),
    path('register/racer/', views.register_racer, name='register_racer'),
    path('register/commentator/', views.register_commentator, name='register_commentator'),

    path('profile/', views.profile, name='profile'),
    path('races/', views.races_list, name='races_list'),
    path('race/<int:race_id>/about/', views.race_about, name='race_about'),
    path('race/<int:race_id>/comments/', views.race_comments, name='race_comments'),
    path('race/<int:race_id>/register/', views.register_for_race, name='race_register'),
    path('race/<int:race_id>/unregister/', views.unregister_from_race, name='race_unregister'),
    path('race/<int:race_id>/results/', views.race_results, name='race_results'),
    path('heat/<int:heat_id>/generate_results/', views.generate_heat_results, name='generate_heat_results'),
]