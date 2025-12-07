from django.urls import path

from .views import ProfileView, UserProfileDetailView

app_name = "accounts"

urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
    path("users/<int:user_id>/profile/", UserProfileDetailView.as_view(), name="user-profile"),
]
