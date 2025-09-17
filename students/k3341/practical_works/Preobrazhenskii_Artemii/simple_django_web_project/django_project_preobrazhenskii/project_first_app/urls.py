from django.urls import path

from . import views

urlpatterns = [
    path("owner/<int:owner_id>/", views.owner_detail, name="owner_detail"),
    path("owners/", views.owners_list, name="owner_list"),
    path("cars/", views.CarListView.as_view(), name="car_list"),
    path("cars/<int:pk>/", views.CarDetailView.as_view(), name="car_detail"),
    path("cars/<int:pk>/update/", views.CarUpdateView.as_view(), name="car_update"),
]