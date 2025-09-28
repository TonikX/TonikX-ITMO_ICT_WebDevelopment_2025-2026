from urllib.parse import urlencode
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView

from .models import Flight, Reservation, Review
from .forms import ReservationForm, ReviewForm


class FlightListView(ListView):
    model = Flight
    template_name = "flights/flight_list.html"
    context_object_name = "flights"
    paginate_by = 7

    def get_queryset(self):
        # Загружаем все объекты Flight и подгружаем объекты airline, airport
        qs = (Flight.objects
              .select_related("airline", "origin_airport", "destination_airport")
              .order_by("departure_time"))

        # Если выбрана фильтрация, то получаем аргументы, по которым нужно фильтровать
        q = self.request.GET.get("q", "").strip()
        t = self.request.GET.get("type")
        airline = self.request.GET.get("airline")
        origin = self.request.GET.get("origin")
        dest = self.request.GET.get("dest")

        # Фильтруем по "ИЛИ"
        if q:
            qs = qs.filter(
                Q(number__icontains=q) |
                Q(airline__name__icontains=q) |
                Q(origin_airport__city__icontains=q) |
                Q(destination_airport__city__icontains=q)
            )
        if t in {"DEPARTURE", "ARRIVAL"}:
            qs = qs.filter(type=t)
        if airline:
            qs = qs.filter(airline__name=airline)
        if origin:
            qs = qs.filter(origin_airport__city=origin)
        if dest:
            qs = qs.filter(destination_airport__city=dest)

        return qs

    # Добавляем в шаблон дополнительные данные
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs) # Получение базового контекста
        ctx["airlines"] = (Flight.objects
                           .select_related("airline")
                           .values_list("airline__name", flat=True)
                           .distinct().order_by("airline__name"))
        ctx["origins"] = (Flight.objects
                          .select_related("origin_airport")
                          .values_list("origin_airport__city", flat=True)
                          .distinct().order_by("origin_airport__city")) # Получаем одномерный список уникальных значений и добавляем в контекст
        ctx["destinations"] = (Flight.objects
                               .select_related("destination_airport")
                               .values_list("destination_airport__city", flat=True)
                               .distinct().order_by("destination_airport__city"))
        
        # Копируем параметры из запроса и удаляем page и преобразовываем в url строку, чтобы в случае пагинации сохранялись фильтры
        params = self.request.GET.copy()
        params.pop("page", None)
        ctx["querystring"] = urlencode(params, doseq=True)
        return ctx

class FlightDetailView(DetailView):
    model = Flight
    template_name = "flights/flight_detail.html"
    context_object_name = "flight"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["my_reservations"] = (
            Reservation.objects.filter(passenger=self.request.user, flight=self.object)
            if self.request.user.is_authenticated else []
        )
        ctx["reviews"] = Review.objects.select_related("author").filter(flight=self.object).order_by("-created_at")
        ctx["passengers"] = Reservation.objects.select_related("passenger").filter(flight=self.object).order_by("seat_number")
        ctx["occupied"] = ctx["passengers"].count()
        ctx["free"] = max(self.object.capacity - ctx["occupied"], 0)
        ctx["my_review_exists"] = (
                self.request.user.is_authenticated
                and Review.objects.filter(flight=self.object, author=self.request.user).exists()
        ) # Проверка, что пользователь авторизован, в таком случае фильтр срабатывает
        return ctx

# Ставим миксины, что пользователь должен быть авторизован и пройден проверку, FormView - обработка post запроса
class FlightStatusUpdateView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'flights/flight_detail.html'

    def post(self, request, *args, **kwargs):
        flight = Flight.objects.get(pk=kwargs['pk'])
        status = request.POST.get('status')
        if status in dict(Flight.STATUS_CHOICES):
            flight.status = status
            flight.save()
        return HttpResponseRedirect(reverse_lazy('flights:flight-detail', kwargs={'pk': flight.pk}))

    # Проверяем, что пользователь - администратор, для изменения статуса полета
    def test_func(self):
        return self.request.user.is_staff

class FlightUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Flight
    fields = ['number', 'departure_time', 'arrival_time', 'gate', 'type', 'capacity']
    template_name = 'flights/flight_update.html'
    success_url = reverse_lazy('flights:flight-list')

    def test_func(self):
        return self.request.user.is_staff

class FlightDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Flight
    template_name = 'flights/flight_delete.html'
    success_url = reverse_lazy('flights:flight-list')

    def test_func(self):
        return self.request.user.is_staff

class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = "flights/reservation_form.html"

    # соаздаем метод, чтобы потом в форму подгрузить id полета
    def dispatch(self, request, *args, **kwargs):
        self.flight = get_object_or_404(Flight, pk=self.kwargs["flight_pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.passenger = self.request.user
        form.instance.flight = self.flight
        try:
            return super().form_valid(form)
        except IntegrityError:
            form.add_error("seat_number", "Место уже занято или вы уже бронировали этот рейс.")
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("flights:flight-detail", kwargs={"pk": self.flight.pk})

class ReservationUpdateView(LoginRequiredMixin, UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = "flights/reservation_form.html"

    # ограничиваем выборку, чтобы были только бронирования пользователя
    def get_queryset(self):
        return Reservation.objects.filter(passenger=self.request.user)

    def get_success_url(self):
        return reverse_lazy("flights:flight-detail", kwargs={"pk": self.object.flight_id})

class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    model = Reservation
    template_name = "flights/reservation_confirm_delete.html"

    def get_queryset(self):
        return Reservation.objects.filter(passenger=self.request.user)

    def get_success_url(self):
        return reverse_lazy("flights:flight-detail", kwargs={"pk": self.object.flight_id})


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "flights/review_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.flight = get_object_or_404(Flight, pk=self.kwargs["flight_pk"])
        # Проверяем существует ли уже отзыв
        if Review.objects.filter(flight=self.flight, author=request.user).exists():
            messages.error(request, "Вы уже оставляли отзыв на этот рейс.")
            return redirect("flights:flight-detail", pk=self.flight.pk)

        current_time = timezone.now()
        if self.flight.arrival_time > current_time:
            messages.error(request, "Вы можете оставить отзыв только на рейс, который уже завершился.")
            return redirect("flights:flight-detail", pk=self.flight.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.flight = self.flight
        form.instance.flight_date = self.flight.departure_time.date()
        try:
            return super().form_valid(form)
        except IntegrityError:
            form.add_error(None, "Вы уже оставляли отзыв на этот рейс.")
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("flights:flight-detail", kwargs={"pk": self.flight.pk})


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('flights:flight-list')
    template_name = 'registration/signup.html'


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('flights:flight-detail', kwargs={'pk': self.object.flight.pk})

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.request.user.is_staff:
            raise PermissionDenied("У вас нет прав для удаления отзыва.")
        self.object.delete()
        return redirect(self.get_success_url())