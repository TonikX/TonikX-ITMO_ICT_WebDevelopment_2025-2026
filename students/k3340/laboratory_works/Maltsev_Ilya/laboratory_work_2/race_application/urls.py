from django.contrib import admin
from django.urls import path

from race_application import views

urlpatterns = [
    path("", views.races_list, name=""),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.dashboard, name='profile'),
    path("registration/", views.registration, name="registration"),
    path("racer_registration/", views.racer_registration, name="racer_registration"),
    path("races/comments/<int:race_id>/", views.race_reviews, name="race_comments"),
    path("races/", views.races_list, name="races_list"),
    path("races_pivot/", views.RacesPivotListView.as_view(), name="races_adm_list"),
    path("create_race_connection/<int:race_id>/", views.create_race_connection, name="create_race_connection"),
    path("delete_race_connection/<int:race_id>", views.delete_race_connection, name="delete_race_connection")
]