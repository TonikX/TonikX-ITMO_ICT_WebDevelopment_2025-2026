from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Конференции
    path("", views.conference_list, name="conference_list"),
    path(
        "conference/<uuid:conference_id>/",
        views.conference_detail,
        name="conference_detail",
    ),
    # Регистрация на конференцию
    path(
        "conference/<uuid:conference_id>/register/",
        views.register_for_conference,
        name="register_for_conference",
    ),
    path(
        "registration/<uuid:registration_id>/edit/",
        views.edit_registration,
        name="edit_registration",
    ),
    path(
        "registration/<uuid:registration_id>/delete/",
        views.delete_registration,
        name="delete_registration",
    ),
    # Комментарии
    path(
        "conference/<uuid:conference_id>/comment/",
        views.add_comment,
        name="add_comment",
    ),
    # Участники
    path("participants/", views.participants_table, name="participants_table"),
    # Аутентификация
    path("register/", views.register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="app/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", views.profile, name="profile"),
]
