from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from .models import Tour
from .forms import ReviewForm
from bookings.models import Booking

class TourListView(ListView):
    model = Tour
    template_name = "tours/tour_list.html"
    context_object_name = "tours"
    paginate_by = 6

    def get_queryset(self):
        qs = (Tour.objects.select_related("agency", "country").order_by("-start_date"))
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(country__name__icontains=q) |
                Q(agency__name__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "").strip()
        return ctx

class TourDetailView(DetailView):
    model = Tour
    template_name = "tours/tour_detail.html"
    context_object_name = "tour"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["form"] = ReviewForm()
        return ctx

class BookTourView(LoginRequiredMixin, DetailView):
    model = Tour

    def post(self, request, *args, **kwargs):
        tour = self.get_object()
        Booking.objects.get_or_create(tour=tour, user=request.user)
        messages.success(request, "Тур забронирован (ожидает подтверждения админом).")
        return redirect("tours:detail", pk=tour.pk)
