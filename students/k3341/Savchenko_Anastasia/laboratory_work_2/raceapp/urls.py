from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'raceapp'  # Пространство имен для URL

urlpatterns = [
    # ===== ОСНОВНЫЕ СТРАНИЦЫ =====
    path('', views.home, name='home'),  # Главная

    # ===== ГОНКИ =====
    path('races/', views.RaceListView.as_view(), name='race_list'),  # Список всех гонок
    path('race/<int:pk>/', views.RaceDetailView.as_view(), name='race_detail'),  # Детали гонки

    # ===== АВТОРИЗАЦИЯ =====
    path('register/', views.register, name='register'),  # Регистрация
    path('login/', views.CustomLoginView.as_view(), name='login'),  # Вход

    # Используем встроенный LogoutView с указанием redirect
    path('logout/', auth_views.LogoutView.as_view(next_page='raceapp:home'), name='logout'),

    # ===== ПОИСК =====
    path('search/', views.search_races, name='search'),  # Поиск гонок

    # ===== РЕГИСТРАЦИЯ НА ГОНКУ =====
    path('racer/register/', views.racer_register, name='racer_register'),  # Форма регистрации
    path('my-registrations/', views.my_registrations, name='my_registrations'),  # Мои регистрации

    # Удаление регистрации (только свои)
    path('racer/delete/<int:pk>/', views.RacerDeleteView.as_view(), name='racer_delete'),

    # ===== КОММЕНТАРИИ =====
    path('race/<int:race_id>/comment/', views.add_comment, name='add_comment'),  # Добавить комментарий
    path('comments/', views.comment_list, name='comment_list'),  # Все комментарии
    path('comment/delete/<int:pk>/', views.delete_comment, name='delete_comment'),  # Удалить комментарий

    # ===== ПРОФИЛЬ =====
    path('profile/', views.profile, name='profile'),  # Просмотр профиля
    path('profile/edit/', views.edit_profile, name='edit_profile'),  # Редактирование профиля

    # ===== ПОДТВЕРЖДЕНИЕ РЕГИСТРАЦИИ (АДМИН) =====
    path('racer/confirm/<int:pk>/', views.confirm_registration, name='confirm_registration'),
]
