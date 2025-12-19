from django.http import Http404
from django.shortcuts import render, redirect
from .models import Hotel, Room, Reservation, Review
from .forms import ReservationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import login
from .forms import CustomUserCreationForm



def hotel_list(request):
    query = request.GET.get('q', '')  # получаем строку поиска (если пустая — ничего не ищем)

    if query:
        hotels_list = Hotel.objects.filter(name__icontains=query)
    else:
        hotels_list = Hotel.objects.all()

    # Пагинация
    paginator = Paginator(hotels_list, 6)  # по 6 отелей на страницу
    page_number = request.GET.get('page')
    hotels = paginator.get_page(page_number)

    # Передаем в шаблон не только отели, но и поисковый запрос, чтобы его сохранить в поле ввода
    return render(request, 'hotel_list.html', {'hotels': hotels, 'query': query})


def hotel_detail(request, hotel_id):
    try:
        hotel = Hotel.objects.get(pk=hotel_id)
    except Hotel.DoesNotExist:
        raise Http404("Отель не найден")

    rooms = Room.objects.filter(hotel=hotel)
    reviews = Review.objects.filter(room__hotel=hotel)
    return render(request, 'hotel_detail.html', {'hotel': hotel, 'rooms': rooms, 'reviews': reviews})

def signup(request):
    """
    Регистрация нового пользователя.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('hotel_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def owner_detail(request, owner_id):
    try:
        owner = User.objects.get(pk=owner_id)
    except User.DoesNotExist:
        raise Http404("Пользователь не найден")
    return render(request, 'owner.html', {'owner': owner})

@user_passes_test(lambda u: u.is_staff)
def recent_guests(request, hotel_id):
    """
    Список постояльцев отеля за последние 30 дней.
    Доступно только для staff-пользователей (админов).
    """
    today = timezone.localdate()
    start_period = today - timedelta(days=30)

    # Получаем выбранный отель из GET-параметра, если не указан — первый по умолчанию
    hotel_id = request.GET.get('hotel_id')
    if hotel_id:
        try:
            hotel = Hotel.objects.get(pk=hotel_id)
        except Hotel.DoesNotExist:
            hotel = None
    else:
        hotel = Hotel.objects.first()  # Если не выбран, берем первый

    residents = []
    if hotel:
        residents = Reservation.objects.filter(
            room__hotel=hotel,
            check_in__lt=today + timedelta(days=1),
            check_out__gt=start_period
        ).order_by('check_in')

    # Получаем список всех отелей для селекта
    hotels = Hotel.objects.all()

    return render(request, 'residents_last_month.html', {
        'hotel': hotel,
        'hotels': hotels,
        'residents': residents,
        'start_period': start_period,
        'end_period': today,
    })

@login_required
def reservation_list(request):
    """
    Список всех бронирований текущего пользователя
    """
    reservations_list = Reservation.objects.filter(user=request.user)
    paginator = Paginator(reservations_list, 6)
    page_number = request.GET.get('page')
    reservations = paginator.get_page(page_number)
    return render(request, 'reservations.html', {'reservations': reservations})


@login_required
def make_reservation(request):
    """
    Создание новой брони
    """
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            return redirect('reservation_list')
    else:
        form = ReservationForm()
    return render(request, 'make_reservation.html', {'form': form})

@login_required
def edit_reservation(request, reservation_id):
    """
    Редактирование существующей брони пользователем
    """
    try:
        reservation = Reservation.objects.get(id=reservation_id, user=request.user)
    except Reservation.DoesNotExist:
        raise Http404("Бронь не найдена или недоступна для редактирования")

    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('reservation_list')
    else:
        form = ReservationForm(instance=reservation)

    return render(request, 'edit_reservation.html', {
        'form': form,
        'reservation': reservation
    })

@login_required
def delete_reservation(request, reservation_id):
    """
    Удаление брони
    """
    try:
        reservation = Reservation.objects.get(id=reservation_id, user=request.user)
    except Reservation.DoesNotExist:
        raise Http404("Бронь не найдена")

    if request.method == 'POST':
        reservation.delete()
        return redirect('reservation_list')

    return render(request, 'delete_reservation.html', {'reservation': reservation})

@login_required
def review_list(request):
    reviews_list = Review.objects.all()
    paginator = Paginator(reviews_list, 6)  # показывать по 6 отзывов на страницу
    page_number = request.GET.get('page')
    reviews = paginator.get_page(page_number)
    return render(request, 'review_list.html', {'reviews': reviews})

@login_required
def add_review(request):
    """
    Добавление нового отзыва к номеру
    """
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        text = request.POST.get('text')
        rating = request.POST.get('rating')
        stay_start = request.POST.get('stay_start')
        stay_end = request.POST.get('stay_end')

        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            raise Http404("Номер не найден")

        # Создаём отзыв
        Review.objects.create(
            user=request.user,
            room=room,
            comment=text,
            rating=rating,
            stay_start = stay_start if stay_start else None,
            stay_end = stay_end if stay_end else None
        )

        # Перенаправляем на страницу отеля после добавления
        return redirect('hotel_detail', hotel_id=room.hotel.id)

    # Если GET-запрос, показываем форму
    rooms = Room.objects.all()
    return render(request, 'add_review.html', {'rooms': rooms})



