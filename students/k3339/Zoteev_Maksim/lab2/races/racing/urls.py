from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("race/<int:race_id>/", views.race_detail, name="race_detail"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("teams/", views.teams_list, name="teams_list"),
    path("cars/", views.cars_list, name="cars_list"),
    # Authentication
    path("register/", views.register_user, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    # Profile
    path("profile/", views.profile, name="profile"),
    path("profile/create/", views.create_profile, name="create_profile"),
    # Race actions
    path(
        "race/<int:race_id>/register/",
        views.register_for_race,
        name="register_for_race",
    ),
    path("race/<int:race_id>/comment/", views.add_comment, name="add_comment"),
    # Admin actions
    path(
        "race/<int:race_id>/manage-results/",
        views.manage_race_results,
        name="manage_race_results",
    ),
]
