from django import forms
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction, IntegrityError
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView

import django_filters
from .models import Flight, Booking, Review


# ------------------ ФИЛЬТРЫ ------------------
class FlightFilter(django_filters.FilterSet):
    """Фильтрация рейсов по направлению, дате и авиакомпании (по коду и названию)."""
    direction = django_filters.CharFilter(field_name='direction', lookup_expr='exact')
    date = django_filters.DateFilter(field_name='departure_dt', lookup_expr='date')
    airline = django_filters.CharFilter(method='filter_airline')

    class Meta:
        model = Flight
        fields = ['direction', 'airline', 'date']

    def filter_airline(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(airline__code__icontains=value) | Q(airline__name__icontains=value)
        )


# ------------------ ФОРМЫ ------------------
class BookingForm(forms.ModelForm):
    ticket_number = forms.CharField(
        label='Номер билета',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Напр., 5551234567890'})
    )

    class Meta:
        model = Booking
        fields = ('ticket_number',)
        labels = {'ticket_number': 'Номер билета'}

    def __init__(self, *args, flight=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.flight = flight

    def save(self, commit=True):
        booking = super().save(commit=False)
        booking.seats_count = 1
        if commit:
            booking.save()
        return booking


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('body', 'rating', 'flight_date')
        widgets = {
            'body': forms.Textarea(attrs={'rows': 4}),
            'flight_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_rating(self):
        r = self.cleaned_data['rating']
        if not (1 <= r <= 10):
            raise forms.ValidationError('Рейтинг должен быть от 1 до 10.')
        return r


# ------------------ ВЬЮХИ ------------------
class FlightListView(ListView):
    model = Flight
    template_name = 'core/flight_list.html'
    context_object_name = 'flights'
    paginate_by = 10

    def get_queryset(self):
        """
        Сначала показываем актуальные (будущие) рейсы,
        а завершённые — внизу таблицы.
        """
        qs = Flight.objects.select_related('airline', 'gate')

        # Фильтрация по параметрам
        filtered = FlightFilter(self.request.GET, queryset=qs).qs

        # Разделяем на предстоящие и завершённые
        now = timezone.now()
        upcoming = filtered.filter(departure_dt__gte=now)
        past = filtered.filter(departure_dt__lt=now)

        # Объединяем: сначала предстоящие, потом прошедшие
        return list(upcoming.order_by('departure_dt')) + list(past.order_by('-departure_dt'))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['filter'] = FlightFilter(self.request.GET, queryset=Flight.objects.none())
        return ctx


class FlightDetailView(DetailView):
    model = Flight
    template_name = 'core/flight_detail.html'
    context_object_name = 'flight'
    pk_url_kwarg = 'flight_id'


@login_required
def create_booking(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)

    if request.method == 'POST':
        ticket_number = (request.POST.get('ticket_number') or '').strip()

        # Проверка на дубль билета для этого рейса
        if Booking.objects.filter(flight=flight, ticket_number=ticket_number).exists():
            messages.error(request, "На этот рейс уже есть бронь с таким номером билета.")
            return redirect('core:flight_detail', flight_id=flight.id)

        # Проверка мест
        if flight.seats_available < 1:
            messages.error(request, "На этот рейс больше нет свободных мест.")
            return redirect('core:flight_detail', flight_id=flight.id)

        try:
            with transaction.atomic():
                Booking.objects.create(
                    user=request.user,
                    flight=flight,
                    seats_count=1,
                    ticket_number=ticket_number
                )
                flight.seats_available -= 1
                flight.save(update_fields=['seats_available'])
        except IntegrityError:
            # если параллельно кто-то уже занял этот ticket_number на этом рейсе
            messages.error(request, "На этот рейс уже есть бронь с таким номером билета.")
            return redirect('core:flight_detail', flight_id=flight.id)

        messages.success(request, f"Вы успешно забронировали место. Номер билета: {ticket_number}")
        return redirect('core:flight_detail', flight_id=flight.id)

    return render(request, 'core/booking_form.html', {'flight': flight})


class MyBookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'core/my_bookings.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return (Booking.objects
                .filter(user=self.request.user)
                .select_related('flight')
                .order_by('-created_at'))


class BookingDeleteView(LoginRequiredMixin, DetailView):
    model = Booking
    template_name = 'core/booking_delete.html'

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != request.user and not request.user.is_staff:
            raise Http404()

        # удаляем бронь и возвращаем места
        with transaction.atomic():
            obj.flight.seats_available = min(
                obj.flight.seats_total,
                obj.flight.seats_available + obj.seats_count
            )
            obj.flight.save(update_fields=['seats_available'])
            obj.delete()

        messages.success(request, "Бронь удалена, место возвращено.")

        # если пришли со страницы пассажиров - вернёмся туда
        next_url = request.POST.get('next') or request.GET.get('next')
        if next_url:
            return redirect(next_url)

        # иначе - в "Мои брони"
        return redirect('core:my_bookings')


@user_passes_test(lambda u: u.is_staff)
def flight_passengers(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    bookings = (Booking.objects
                .filter(flight=flight)
                .select_related('user')
                .order_by('-created_at'))
    return render(request, 'core/flight_passengers.html', {'flight': flight, 'bookings': bookings})


@login_required
def create_review(request, pk):
    flight = get_object_or_404(Flight, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rv = form.save(commit=False)
            rv.author = request.user
            rv.flight = flight
            rv.save()
            messages.success(request, "Спасибо! Отзыв добавлен.")
            return redirect('core:flight_detail', flight_id=pk)
    else:
        form = ReviewForm(initial={'flight_date': timezone.now().date()})
    return render(request, 'core/review_form.html', {'form': form, 'flight': flight})


@login_required
def review_delete(request, flight_id, pk):
    """
    Удаление отзыва. Разрешено автору отзыва и staff.
    После удаления возвращаемся на страницу рейса.
    """
    flight = get_object_or_404(Flight, id=flight_id)
    review = get_object_or_404(Review, id=pk, flight=flight)

    if review.author != request.user and not request.user.is_staff:
        messages.error(request, "Удаление запрещено.")
        return redirect('core:flight_detail', flight_id=flight.id)

    if request.method == 'POST':
        review.delete()
        messages.success(request, "Отзыв удалён.")
        return redirect('core:flight_detail', flight_id=flight.id)

    return redirect('core:flight_detail', flight_id=flight.id)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Аккаунт создан! Добро пожаловать 👋")
            return redirect('core:flight_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def bookings_list(request):
    bookings = Booking.objects.filter(user=request.user).select_related('flight')
    return render(request, 'core/bookings_list.html', {'bookings': bookings})


User = get_user_model()


class BookingAdminForm(forms.ModelForm):
    """Форма для создания брони админом на конкретный рейс."""
    user = forms.ModelChoiceField(queryset=User.objects.all(), label='Пользователь')
    seats_count = forms.IntegerField(min_value=1, initial=1, label='Мест')

    class Meta:
        model = Booking
        fields = ('user', 'ticket_number', 'seats_count')
        labels = {
            'ticket_number': '№ билета',
            'seats_count': 'Мест',
        }


@user_passes_test(lambda u: u.is_staff)
def flight_add_passenger(request, flight_id):
    """
    Админ добавляет пассажира на рейс.
    - проверяем уникальность (flight, ticket_number)
    - проверяем наличие мест
    """
    flight = get_object_or_404(Flight, id=flight_id)

    if request.method == 'POST':
        form = PassengerAddForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.flight = flight

            if not getattr(booking, 'seats_count', None):
                booking.seats_count = 1

            booking.ticket_number = (booking.ticket_number or '').strip()

            # 1) дубль билета на этот рейс
            if Booking.objects.filter(
                flight=flight,
                ticket_number=booking.ticket_number
            ).exists():
                form.add_error('ticket_number', 'Билет с таким номером уже есть на этом рейсе.')
            # 2) нет мест
            elif flight.seats_available < booking.seats_count:
                form.add_error(None, 'Недостаточно свободных мест.')
            else:
                try:
                    with transaction.atomic():
                        booking.save()
                        # уменьшаем места
                        flight.seats_available -= booking.seats_count
                        if flight.seats_available < 0:
                            raise IntegrityError("Недостаточно мест")
                        flight.save(update_fields=['seats_available'])
                    messages.success(request, 'Пассажир(ы) добавлен(ы).')
                    return redirect('core:flight_passengers', flight_id=flight.id)
                except IntegrityError:
                    form.add_error('ticket_number', 'Билет с таким номером уже есть на этом рейсе.')
    else:
        form = PassengerAddForm()

    return render(request, 'core/passenger_add_form.html', {
        'form': form,
        'flight': flight,
    })


@user_passes_test(lambda u: u.is_staff)
def flight_delete_passenger(request, flight_id, booking_id):
    """
    Админ удаляет бронь конкретного пассажира у указанного рейса.
    Возвращаем места в рейс.
    """
    flight = get_object_or_404(Flight, id=flight_id)
    booking = get_object_or_404(Booking, id=booking_id, flight=flight)

    if request.method == 'POST':
        with transaction.atomic():
            flight.seats_available = min(
                flight.seats_total,
                flight.seats_available + booking.seats_count
            )
            flight.save(update_fields=['seats_available'])
            booking.delete()
        messages.success(request, "Бронь пассажира удалена, места возвращены.")
        return redirect('core:flight_passengers', flight_id=flight.id)

    return render(
        request,
        'core/passenger_confirm_delete.html',
        {'flight': flight, 'booking': booking}
    )


# --- ФОРМА для добавления пассажира админом ---
class PassengerAddForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('user', 'ticket_number')
        labels = {
            'user': 'Пользователь',
            'ticket_number': '№ билета',
        }
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'ticket_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Напр., 5551234567890'
            }),
        }

    def save(self, commit=True):
        booking = super().save(commit=False)
        booking.seats_count = 1
        if commit:
            booking.save()
        return booking
