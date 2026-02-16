from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.homework_list, name="homework_list"),
    path("homework/<int:homework_id>/", views.homework_detail, name="homework_detail"),
    path("homework/<int:homework_id>/submit/", views.submit_homework, name="submit_homework"),

    path("register/", views.register_view, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="board/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    path("class-grades/", views.class_grades_table, name="class_grades_table"),
    path("my-grades/", views.my_grades, name="my_grades"),
]
