from django.urls import path
from . import views

urlpatterns = [
    path("owners/", views.OwnerListCreateAPIView.as_view(), name="owners-list"),
    path("owners/<int:pk>/", views.OwnerRetrieveUpdateDestroyAPIView.as_view(), name="owner-detail"),

    path("cars/", views.CarListCreateAPIView.as_view(), name="cars-list"),
    path("cars/<int:pk>/", views.CarRetrieveUpdateDestroyAPIView.as_view(), name="car-detail"),

    path("ownerships/", views.OwnershipListCreateAPIView.as_view(), name="ownerships-list"),
    path("ownerships/<int:pk>/", views.OwnershipRetrieveUpdateDestroyAPIView.as_view(), name="ownership-detail"),

    path("owners/<int:owner_id>/cars/", views.CarsByOwnerAPIView.as_view(), name="owner-cars"),
    path("cars/<int:car_id>/owners/", views.OwnersByCarAPIView.as_view(), name="car-owners"),
]
