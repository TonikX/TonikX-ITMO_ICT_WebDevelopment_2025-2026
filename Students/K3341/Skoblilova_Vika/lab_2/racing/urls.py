"""
URL patterns для приложения racing.
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Главная - список гонок
    path('', views.RaceListView.as_view(), name='race_list'),
    path('race/<int:pk>/', views.RaceDetailView.as_view(), name='race_detail'),
    
    # Регистрация на гонки
    path('race/<int:pk>/register/', views.register_for_race, name='register_for_race'),
    path('race/<int:pk>/unregister/', views.unregister_from_race, name='unregister_from_race'),
    path('registrations/', views.RegistrationListView.as_view(), name='registration_list'),
    path('registration/<int:pk>/edit/', views.RegistrationUpdateView.as_view(), name='registration_update'),
    path('registration/<int:pk>/delete/', views.RegistrationDeleteView.as_view(), name='registration_delete'),
    
    # Комментарии
    path('race/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    
    # Профиль водителя
    path('profile/', views.DriverProfileDetailView.as_view(), name='driverprofile_detail'),
    path('profile/edit/', views.DriverProfileUpdateView.as_view(), name='driverprofile_update'),
    
    # Аутентификация
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change.html',
        success_url='/password_change/done/'
    ), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'
    ), name='password_change_done'),
]

