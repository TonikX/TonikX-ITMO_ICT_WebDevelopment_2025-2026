from django.urls import path
from .views import MyBookingsView, BookingDeleteView
from .views_sales import SalesByCountryView

app_name = "bookings"

urlpatterns = [
    path("mine/", MyBookingsView.as_view(), name="mine"),
    path("<int:pk>/delete/", BookingDeleteView.as_view(), name="delete"),
    path("sales-by-country/", SalesByCountryView.as_view(), name="sales_by_country"),
]
