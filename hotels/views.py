from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from .models import Hotel, RoomType, Reservation, Review
from .forms import UserRegistrationForm, ReservationForm, ReviewForm


def home(request):
    """Главная страница со списком отелей"""
    hotels = Hotel.objects.all()
    return render(request, 'hotels/home.html', {'hotels': hotels})


def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'hotels/register.html', {'form': form})


def user_login(request):
    """Вход пользователя"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему!')
            return redirect('home')
        else:
            messages.error(request, 'Неверный логин или пароль')
    return render(request, 'hotels/login.html')


def user_logout(request):
    """Выход пользователя"""
    logout(request)
    messages.success(request, 'Вы вышли из системы')
    return redirect('home')


def hotel_detail(request, hotel_id):
    """Детальная информация об отеле"""
    hotel = get_object_or_404(Hotel, id=hotel_id)
    room_types = hotel.room_types.all().annotate(avg_rating=Avg('reviews__rating'))
    return render(request, 'hotels/hotel_detail.html', {
        'hotel': hotel,
        'room_types': room_types
    })


def room_detail(request, room_id):
    """Детальная информация о типе номера"""
    room_type = get_object_or_404(RoomType, id=room_id)
    reviews = room_type.reviews.all().select_related('user')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    
    return render(request, 'hotels/room_detail.html', {
        'room_type': room_type,
        'reviews': reviews,
        'avg_rating': avg_rating
    })


@login_required
def create_reservation(request, room_id):
    """Создание резервирования"""
    room_type = get_object_or_404(RoomType, id=room_id)
    
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.room_type = room_type
            reservation.status = 'pending'
            reservation.save()
            messages.success(request, 'Резервирование создано успешно!')
            return redirect('my_reservations')
    else:
        form = ReservationForm()
    
    return render(request, 'hotels/create_reservation.html', {
        'form': form,
        'room_type': room_type
    })


@login_required
def my_reservations(request):
    """Список резервирований пользователя"""
    reservations = request.user.reservations.all().select_related('room_type__hotel')
    return render(request, 'hotels/my_reservations.html', {'reservations': reservations})


@login_required
def edit_reservation(request, reservation_id):
    """Редактирование резервирования"""
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    
    # Можно редактировать только ожидающие подтверждения резервирования
    if reservation.status != 'pending':
        messages.error(request, 'Можно редактировать только резервирования в статусе "Ожидает подтверждения"')
        return redirect('my_reservations')
    
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Резервирование обновлено')
            return redirect('my_reservations')
    else:
        form = ReservationForm(instance=reservation)
    
    return render(request, 'hotels/edit_reservation.html', {
        'form': form,
        'reservation': reservation
    })


@login_required
def delete_reservation(request, reservation_id):
    """Удаление резервирования"""
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    
    # Можно удалять только ожидающие подтверждения резервирования
    if reservation.status != 'pending':
        messages.error(request, 'Можно удалять только резервирования в статусе "Ожидает подтверждения"')
        return redirect('my_reservations')
    
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, 'Резервирование удалено')
        return redirect('my_reservations')
    
    return render(request, 'hotels/delete_reservation.html', {'reservation': reservation})


@login_required
def add_review(request, room_id):
    """Добавление отзыва"""
    room_type = get_object_or_404(RoomType, id=room_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.room_type = room_type
            review.save()
            messages.success(request, 'Отзыв добавлен!')
            return redirect('room_detail', room_id=room_id)
    else:
        form = ReviewForm()
    
    return render(request, 'hotels/add_review.html', {
        'form': form,
        'room_type': room_type
    })


def recent_guests(request):
    """Таблица постояльцев за последний месяц"""
    guests = Reservation.get_recent_guests()
    
    # Группировка по отелям для удобства
    hotels_data = {}
    for reservation in guests:
        hotel_name = reservation.room_type.hotel.name
        if hotel_name not in hotels_data:
            hotels_data[hotel_name] = []
        hotels_data[hotel_name].append(reservation)
    
    return render(request, 'hotels/recent_guests.html', {'hotels_data': hotels_data})
