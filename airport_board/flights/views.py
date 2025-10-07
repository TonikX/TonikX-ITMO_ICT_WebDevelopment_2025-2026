from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
import json
from .models import Flight, Reservation, Passenger, Review
from .forms import UserRegistrationForm, ReservationForm, ReviewForm, PassengerRegistrationForm


def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('flight_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'flights/register.html', {'form': form})


def flight_list(request):
    """Список всех рейсов"""
    flights = Flight.objects.all()
    
    # Добавляем средний рейтинг для каждого рейса
    for flight in flights:
        avg_rating = flight.reviews.aggregate(Avg('rating'))['rating__avg']
        flight.avg_rating = round(avg_rating, 1) if avg_rating else None
    
    return render(request, 'flights/flight_list.html', {'flights': flights})


def flight_detail(request, pk):
    """Детальная информация о рейсе"""
    flight = get_object_or_404(Flight, pk=pk)
    reviews = flight.reviews.all()
    avg_rating = flight.reviews.aggregate(Avg('rating'))['rating__avg']
    
    # Проверяем, есть ли у пользователя резервирование на этот рейс
    user_reservation = None
    if request.user.is_authenticated:
        user_reservation = Reservation.objects.filter(
            user=request.user,
            flight=flight,
            is_active=True
        ).first()
    
    context = {
        'flight': flight,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1) if avg_rating else None,
        'user_reservation': user_reservation
    }
    return render(request, 'flights/flight_detail.html', context)


@login_required
def make_reservation(request, flight_id):
    """Создание резервирования"""
    flight = get_object_or_404(Flight, pk=flight_id)
    
    # Проверяем, есть ли у пользователя уже резервирование на этот рейс
    existing = Reservation.objects.filter(
        user=request.user,
        flight=flight,
        is_active=True
    ).exists()
    
    if existing:
        messages.warning(request, 'У вас уже есть резервирование на этот рейс.')
        return redirect('flight_detail', pk=flight_id)
    
    # Проверяем наличие свободных мест
    if flight.available_seats() <= 0:
        messages.error(request, 'К сожалению, на этом рейсе нет свободных мест.')
        return redirect('flight_detail', pk=flight_id)
    
    # Получаем список занятых мест
    occupied_seats = list(Reservation.objects.filter(
        flight=flight,
        is_active=True,
        seat_number__isnull=False
    ).exclude(seat_number='').values_list('seat_number', flat=True))
    
    if request.method == 'POST':
        form = ReservationForm(request.POST, flight=flight)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.flight = flight
            reservation.save()
            messages.success(request, 'Резервирование создано успешно!')
            return redirect('my_reservations')
    else:
        form = ReservationForm(flight=flight)
    
    return render(request, 'flights/make_reservation.html', {
        'form': form,
        'flight': flight,
        'occupied_seats': json.dumps(occupied_seats)
    })


@login_required
def my_reservations(request):
    """Список резервирований пользователя"""
    reservations = Reservation.objects.filter(
        user=request.user,
        is_active=True
    ).select_related('flight')
    return render(request, 'flights/my_reservations.html', {
        'reservations': reservations
    })


@login_required
def edit_reservation(request, pk):
    """Редактирование резервирования"""
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    flight = reservation.flight
    
    # Получаем список занятых мест (кроме текущего резервирования)
    occupied_seats = list(Reservation.objects.filter(
        flight=flight,
        is_active=True,
        seat_number__isnull=False
    ).exclude(seat_number='').exclude(pk=reservation.pk).values_list('seat_number', flat=True))
    
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation, flight=reservation.flight)
        if form.is_valid():
            form.save()
            messages.success(request, 'Резервирование обновлено!')
            return redirect('my_reservations')
    else:
        form = ReservationForm(instance=reservation, flight=reservation.flight)
    
    return render(request, 'flights/edit_reservation.html', {
        'form': form,
        'reservation': reservation,
        'flight': flight,
        'occupied_seats': json.dumps(occupied_seats),
        'current_seat': reservation.seat_number or ''
    })


@login_required
def delete_reservation(request, pk):
    """Удаление резервирования"""
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    
    if request.method == 'POST':
        reservation.is_active = False
        reservation.save()
        messages.success(request, 'Резервирование отменено.')
        return redirect('my_reservations')
    
    return render(request, 'flights/delete_reservation.html', {
        'reservation': reservation
    })


def passengers_list(request, flight_id):
    """Список пассажиров рейса"""
    flight = get_object_or_404(Flight, pk=flight_id)
    passengers = Passenger.objects.filter(
        reservation__flight=flight,
        reservation__is_active=True
    ).select_related('reservation__user')
    
    return render(request, 'flights/passengers_list.html', {
        'flight': flight,
        'passengers': passengers
    })


@login_required
def add_review(request, flight_id):
    """Добавление отзыва к рейсу"""
    flight = get_object_or_404(Flight, pk=flight_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.flight = flight
            review.save()
            messages.success(request, 'Отзыв добавлен!')
            return redirect('flight_detail', pk=flight_id)
    else:
        # Автозаполнение даты рейса из даты отлета
        initial_data = {'flight_date': flight.departure_time.date()}
        form = ReviewForm(initial=initial_data)
    
    return render(request, 'flights/add_review.html', {
        'form': form,
        'flight': flight
    })


@login_required
def register_passenger(request, reservation_id):
    """Регистрация пассажира на рейс"""
    reservation = get_object_or_404(Reservation, pk=reservation_id, user=request.user, is_active=True)
    
    # Проверяем, нет ли уже зарегистрированного пассажира
    if hasattr(reservation, 'passenger'):
        messages.warning(request, 'Вы уже зарегистрированы на этот рейс!')
        return redirect('my_reservations')
    
    if request.method == 'POST':
        form = PassengerRegistrationForm(request.POST)
        if form.is_valid():
            passenger = form.save(commit=False)
            passenger.reservation = reservation
            passenger.save()
            messages.success(request, 'Регистрация на рейс завершена успешно!')
            return redirect('my_reservations')
    else:
        # Автозаполнение имени и фамилии из профиля пользователя
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name
        }
        form = PassengerRegistrationForm(initial=initial_data)
    
    return render(request, 'flights/register_passenger.html', {
        'form': form,
        'reservation': reservation,
        'flight': reservation.flight
    })
