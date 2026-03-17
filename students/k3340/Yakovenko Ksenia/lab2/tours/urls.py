from django.urls import path
from .views import TourListView, TourDetailView, BookTourView
from .views_reviews import ReviewCreateView

app_name = "tours"

urlpatterns = [
    path("", TourListView.as_view(), name="list"),
    path("tours/<int:pk>/", TourDetailView.as_view(), name="detail"),
    path("tours/<int:pk>/book/", BookTourView.as_view(), name="book"),
    path("tours/<int:pk>/review/", ReviewCreateView.as_view(), name="review_create"),
]
