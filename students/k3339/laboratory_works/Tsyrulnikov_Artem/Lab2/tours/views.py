from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView

from .forms import ReservationForm, ReviewForm, UserRegistrationForm
from .models import Reservation, Review, Tour


class TourListView(ListView):
    model = Tour
    template_name = "tours/tour_list.html"
    context_object_name = "tours"


class TourDetailView(DetailView):
    model = Tour
    template_name = "tours/tour_detail.html"
    context_object_name = "tour"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["reviews"] = Review.objects.filter(tour=self.object)
        ctx["form"] = ReviewForm()
        return ctx


def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("tours:list")
    else:
        form = UserRegistrationForm()
    return render(request, "tours/register.html", {"form": form})


@login_required
def reserve_tour(request: HttpRequest, pk: int) -> HttpResponse:
    tour = get_object_or_404(Tour, pk=pk)
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.tour = tour
            reservation.save()
            messages.success(request, "Заявка отправлена, ожидайте подтверждения администратора.")
            return redirect("tours:my_reservations")
    else:
        form = ReservationForm(
            initial={"travel_start": tour.start_date, "travel_end": tour.end_date}
        )
    return render(request, "tours/reservation_form.html", {"form": form, "tour": tour})


@login_required
def my_reservations(request: HttpRequest) -> HttpResponse:
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, "tours/reservations.html", {"reservations": reservations})


@login_required
def reservation_update(request: HttpRequest, pk: int) -> HttpResponse:
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    if request.method == "POST":
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, "Бронирование обновлено.")
            return redirect("tours:my_reservations")
    else:
        form = ReservationForm(instance=reservation)
    return render(
        request,
        "tours/reservation_form.html",
        {"form": form, "tour": reservation.tour, "edit_mode": True},
    )


@login_required
def reservation_delete(request: HttpRequest, pk: int) -> HttpResponse:
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    if request.method == "POST":
        reservation.delete()
        messages.info(request, "Бронирование удалено.")
        return redirect("tours:my_reservations")
    return render(request, "tours/reservation_confirm_delete.html", {"reservation": reservation})


@login_required
def add_review(request: HttpRequest, pk: int) -> HttpResponse:
    tour = get_object_or_404(Tour, pk=pk)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.tour = tour
            review.author = request.user
            review.save()
            messages.success(request, "Спасибо за отзыв!")
    return redirect("tours:detail", pk=pk)


class SalesByCountryView(LoginRequiredMixin, ListView):
    template_name = "tours/sales.html"
    context_object_name = "totals"
    login_url = reverse_lazy("tours:login")

    def get_queryset(self):
        return Reservation.objects.filter(status=Reservation.CONFIRMED).values(
            "tour__country"
        ).annotate(total=Count("id")).order_by("tour__country")


@login_required
def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    messages.info(request, "Вы вышли из системы.")
    return redirect("tours:list")
