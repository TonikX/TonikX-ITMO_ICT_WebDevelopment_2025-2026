from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView
from .models import Booking

class MyBookingsView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = "bookings/my_bookings.html"
    context_object_name = "bookings"

    def get_queryset(self):
        return (Booking.objects
                .select_related("tour", "tour__country", "tour__agency")
                .filter(user=self.request.user)
                .order_by("-created_at"))

class BookingDeleteView(LoginRequiredMixin, DeleteView):
    model = Booking
    template_name = "bookings/booking_confirm_delete.html"
    success_url = reverse_lazy("bookings:mine")

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
