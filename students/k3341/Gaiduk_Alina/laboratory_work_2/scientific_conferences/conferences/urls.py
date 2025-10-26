from django.urls import path
from . import views


urlpatterns = [
    path("", views.conference_list, name="conference_list"),
    path("<int:pk>/", views.conference_detail, name="conference_detail"),
    path("<int:pk>/register/", views.register_for_conference, name="register_for_conference"),
    path("registration/<int:pk>/delete/", views.delete_registration, name="delete_registration"),
    path("<int:pk>/review/", views.add_review, name="add_review"),
]