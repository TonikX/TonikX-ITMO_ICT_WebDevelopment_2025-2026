from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from .views import signup

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("tours.urls")),
    path("bookings/", include("bookings.urls")),

    path("signup/", signup, name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    path("accounts/profile/", TemplateView.as_view(template_name="profile.html"), name="profile"),
]
