from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import LoginForm

app_name = "tours"

urlpatterns = [
    path("", views.TourListView.as_view(), name="list"),
    path("tour/<int:pk>/", views.TourDetailView.as_view(), name="detail"),
    path("tour/<int:pk>/reserve/", views.reserve_tour, name="reserve"),
    path("tour/<int:pk>/review/", views.add_review, name="review"),
    path("reservations/", views.my_reservations, name="my_reservations"),
    path("reservations/<int:pk>/edit/", views.reservation_update, name="reservation_edit"),
    path("reservations/<int:pk>/delete/", views.reservation_delete, name="reservation_delete"),
    path("sales/", views.SalesByCountryView.as_view(), name="sales"),
    path("register/", views.register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="tours/login.html", authentication_form=LoginForm),
        name="login",
    ),
    path("logout/", views.logout_view, name="logout"),
]
