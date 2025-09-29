from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Flight, Reservation, Review, UserProfile
from .forms import ReservationForm, ReviewForm, UserProfileForm
import random
import string


def flight_list(request):
    """Список всех рейсов с поиском и фильтрацией"""
    flights = Flight.objects.select_related('airline').prefetch_related('reviews').order_by('departure_time')
    
    # Поиск
    search_query = request.GET.get('search', '')
    if search_query:
        flights = flights.filter(
            Q(flight_number__icontains=search_query) |
            Q(airline__name__icontains=search_query) |
            Q(origin__icontains=search_query) |
            Q(destination__icontains=search_query)
        )
    
    # Фильтрация по типу рейса
    flight_type = request.GET.get('type', '')
    if flight_type:
        flights = flights.filter(flight_type=flight_type)
    
    # Добавляем средний рейтинг для каждого рейса
    flights = flights.annotate(avg_rating=Avg('reviews__rating'))
    
    # Пагинация
    paginator = Paginator(flights, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'flight_type': flight_type,
    }
    return render(request, 'flights/flight_list.html', context)


def flight_detail(request, flight_id):
    """Детальная информация о рейсе"""
    flight = get_object_or_404(Flight, id=flight_id)
    reviews = flight.reviews.select_related('user').order_by('-created_at')
    passengers = flight.reservations.select_related('user').order_by('seat_number')
    
    # Получаем все резервирования пользователя на этот рейс
    user_reservations = []
    if request.user.is_authenticated:
        user_reservations = flight.reservations.filter(user=request.user).order_by('seat_number')
    
    context = {
        'flight': flight,
        'reviews': reviews,
        'passengers': passengers,
        'user_reservations': user_reservations,
        'available_seats': flight.available_seats,
    }
    return render(request, 'flights/flight_detail.html', context)


@login_required
def make_reservation(request, flight_id):
    """Создание резервирования"""
    flight = get_object_or_404(Flight, id=flight_id)
    
    # Пользователь может бронировать несколько мест
    
    if request.method == 'POST':
        form = ReservationForm(request.POST, flight=flight)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.flight = flight
            
            # Генерируем номер билета
            reservation.ticket_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            reservation.save()
            
            messages.success(request, f'Место {reservation.seat_number} успешно забронировано! Номер билета: {reservation.ticket_number}')
            return redirect('flight_detail', flight_id=flight_id)
    else:
        form = ReservationForm(flight=flight)
    
    context = {
        'form': form,
        'flight': flight,
    }
    return render(request, 'flights/make_reservation.html', context)


@login_required
def edit_reservation(request, reservation_id):
    """Редактирование резервирования"""
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation, flight=reservation.flight)
        if form.is_valid():
            form.save()
            messages.success(request, 'Резервирование успешно изменено!')
            return redirect('flight_detail', flight_id=reservation.flight.id)
    else:
        form = ReservationForm(instance=reservation, flight=reservation.flight)
    
    context = {
        'form': form,
        'reservation': reservation,
        'flight': reservation.flight,
    }
    return render(request, 'flights/edit_reservation.html', context)


@login_required
def cancel_reservation(request, reservation_id):
    """Отмена резервирования"""
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    flight_id = reservation.flight.id
    
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, 'Резервирование отменено.')
        return redirect('flight_detail', flight_id=flight_id)
    
    context = {
        'reservation': reservation,
    }
    return render(request, 'flights/cancel_reservation.html', context)


@login_required
def add_review(request, flight_id):
    """Добавление отзыва о рейсе"""
    flight = get_object_or_404(Flight, id=flight_id)
    
    # Проверяем, нет ли уже отзыва от пользователя
    if Review.objects.filter(user=request.user, flight=flight).exists():
        messages.error(request, 'Вы уже оставили отзыв на этот рейс.')
        return redirect('flight_detail', flight_id=flight_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.flight = flight
            review.save()
            messages.success(request, 'Отзыв добавлен!')
            return redirect('flight_detail', flight_id=flight_id)
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'flight': flight,
    }
    return render(request, 'flights/add_review.html', context)


def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            
            # Получаем или создаем профиль пользователя
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'phone': profile_form.cleaned_data.get('phone', ''),
                    'address': profile_form.cleaned_data.get('address', ''),
                }
            )
            
            # Если профиль уже существовал, обновляем его данные
            if not created:
                profile.phone = profile_form.cleaned_data.get('phone', '')
                profile.address = profile_form.cleaned_data.get('address', '')
                profile.save()
            
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('flight_list')
    else:
        form = UserCreationForm()
        profile_form = UserProfileForm()
    
    context = {
        'form': form,
        'profile_form': profile_form,
    }
    return render(request, 'registration/register.html', context)


@login_required
def user_reservations(request):
    """Список резервирований пользователя"""
    reservations = Reservation.objects.filter(user=request.user).select_related('flight__airline').order_by('-created_at')
    
    context = {
        'reservations': reservations,
    }
    return render(request, 'flights/user_reservations.html', context)