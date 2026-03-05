from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count, Q
from django.db.models.functions import Lower
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView

from .forms import ReservationCreateForm, ReviewCreateForm
from .models import Tour, Reservation, Agency, Review


class AgencyListView(ListView):
    model = Agency
    template_name = "agency/agencies.html"
    context_object_name = "agencies"


def agency_tours(request, agency_id):
    agency = get_object_or_404(Agency, id=agency_id)
    tours = Tour.objects.filter(agency=agency)
    return render(request, "agency/agency_tours.html", {"agency": agency, "tours": tours})


class TourListView(ListView):
    model = Tour
    template_name = "tour/tours.html"
    context_object_name = "tours"
    paginate_by = 6

    def get_queryset(self):
        queryset = Tour.objects.all()
        search_query = self.request.GET.get("search", "")
        country_filter = self.request.GET.get("country", "")

        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        if country_filter:
            queryset = queryset.filter(country=country_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("search", "")
        context["country_filter"] = self.request.GET.get("country", "")

        context["countries"] = Tour.objects.values_list("country", flat=True).distinct()

        return context


@login_required(login_url='/login/')
class ReservationDeleteView(DeleteView):
    model = Reservation
    template_name = 'reservation/reservation_delete.html'
    success_url = reverse_lazy('reservations')

    def get_object(self, queryset=None):
        return get_object_or_404(Reservation, id=self.kwargs['pk'], user=self.request.user)


@login_required(login_url='/login/')
def create_reservation(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    user = request.user
    if Reservation.objects.filter(user=user, tour=tour).exists():
        return redirect("reservations")  # Запрещаем повторное бронирование
    form = ReservationCreateForm(request.POST or None)
    if form.is_valid():
        reservation = form.save(commit=False)
        reservation.user = user
        reservation.tour = tour
        reservation.save()
        return redirect("/reservations/")
    return render(request, "reservation/reservation_create.html", {"form": form, "tour": tour})


@login_required(login_url='/login/')
def user_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, "reservation/reservations.html", {"reservations": reservations})


@user_passes_test(lambda u: u.is_superuser)
def pending_reservations(request):
    reservations = Reservation.objects.filter(status='pending')
    return render(request, 'reservation/pending_reservations.html', {'reservations': reservations})


@user_passes_test(lambda u: u.is_superuser)
def update_reservation_status(request, pk, new_status):
    reservation = get_object_or_404(Reservation, pk=pk)
    reservation.status = new_status
    reservation.save()
    return redirect('pending_reservations')


class TourReviewsView(ListView):
    model = Review
    template_name = "tour/reviews.html"
    context_object_name = "reviews"

    def get_queryset(self):
        tour_id = self.kwargs['tour_id']
        return Review.objects.filter(reservation__tour_id=tour_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tour = get_object_or_404(Tour, id=self.kwargs['tour_id'])
        context['tour'] = tour
        context['user_has_reservation'] = self.request.user.is_authenticated and tour.reservation_set.filter(
            user=self.request.user, status="approved").exists()
        return context


from django.http import HttpResponseForbidden


@login_required(login_url="/login/")
def create_review(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    reservation = Reservation.objects.filter(user=request.user, tour=tour, status="approved").first()

    if not reservation:
        return HttpResponseForbidden("Вы не можете оставить отзыв, так как не бронировали этот тур.")

    if request.method == "POST":
        form = ReviewCreateForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reservation = reservation
            review.user = request.user
            review.save()
            return redirect('tour_reviews', tour_id=tour.id)
    else:
        form = ReviewCreateForm()

    return render(request, "tour/review_create.html", {"form": form, "tour": tour})


@login_required(login_url="/login/")
def sold_tours_by_country(request):
    sold_tours = (
        Reservation.objects.filter(status="approved")
        .values("tour__country")
        .annotate(total=Count("id"))
        .order_by("-total")
    )
    return render(request, "report/sold_tours_by_country.html", {"sold_tours": sold_tours})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/login/")
    else:
        form = UserCreationForm()
    return render(request, "account/register.html", {"form": form})


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("/reservations/")
    return render(request, "account/login.html")
