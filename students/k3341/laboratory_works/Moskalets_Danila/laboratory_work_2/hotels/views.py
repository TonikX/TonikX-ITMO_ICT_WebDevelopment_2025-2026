from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Hotel, RoomType, Reservation, Review
from .forms import ReservationForm, ReviewForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.utils import timezone
from datetime import timedelta
from django.contrib.admin.views.decorators import staff_member_required


def home(request):
    hotels_list = Hotel.objects.all().order_by('name')

    search_query = request.GET.get('search', '')
    if search_query:
        hotels_list = hotels_list.filter(
            Q(name__icontains=search_query) |
            Q(owner__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    paginator = Paginator(hotels_list, 6)
    page = request.GET.get('page', 1)

    try:
        hotels = paginator.page(page)
    except PageNotAnInteger:
        hotels = paginator.page(1)
    except EmptyPage:
        hotels = paginator.page(paginator.num_pages)

    return render(request, 'hotels/home.html', {
        'hotels': hotels,
        'search_query': search_query
    })


@login_required
def my_reservations(request):
    reservations_list = Reservation.objects.filter(user=request.user).order_by('-created_at')

    paginator = Paginator(reservations_list, 5)
    page = request.GET.get('page', 1)

    try:
        reservations = paginator.page(page)
    except PageNotAnInteger:
        reservations = paginator.page(1)
    except EmptyPage:
        reservations = paginator.page(paginator.num_pages)

    return render(request, 'hotels/my_reservations.html', {
        'reservations': reservations
    })


def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    room_types = hotel.room_types.all()

    reviews = Review.objects.filter(
        reservation__room_type__hotel=hotel
    ).select_related('reservation__user').order_by('-created_at')[:5]

    room_search = request.GET.get('room_search', '')
    if room_search:
        room_types = room_types.filter(name__icontains=room_search)
        try:
            max_price = float(room_search)
            room_types = room_types.filter(price__lte=max_price)
        except (ValueError, TypeError):
            pass

    return render(request, 'hotels/hotel_detail.html', {
        'hotel': hotel,
        'room_types': room_types,
        'room_search': room_search,
        'reviews': reviews
    })


def room_type_detail(request, room_type_id):
    room_type = get_object_or_404(RoomType, id=room_type_id)
    reservations = Reservation.objects.filter(
        room_type=room_type,
        status__in=['confirmed', 'checked_in']
    )

    return render(request, 'hotels/room_type_detail.html', {
        'room_type': room_type,
        'reservations': reservations
    })



@login_required
def make_reservation(request, room_type_id):
    room_type = get_object_or_404(RoomType, id=room_type_id)

    occupied_reservations = Reservation.objects.filter(
        room_type=room_type,
        status__in=['pending', 'confirmed', 'checked_in']
    )

    occupied_dates = []
    for reservation in occupied_reservations:
        occupied_dates.append({
            'start': reservation.check_in.isoformat(),
            'end': reservation.check_out.isoformat(),
            'text': f"{reservation.check_in.strftime('%d.%m')}-{reservation.check_out.strftime('%d.%m')}"
        })

    if request.method == 'POST':
        form = ReservationForm(request.POST, room_type=room_type)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.room_type = room_type
            reservation.save()
            messages.success(request, 'Бронирование успешно создано!')
            return redirect('my_reservations')
    else:
        form = ReservationForm(room_type=room_type)

    return render(request, 'hotels/make_reservation.html', {
        'form': form,
        'room_type': room_type,
        'occupied_dates': occupied_dates
    })


@login_required
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)

    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation, room_type=reservation.room_type)
        if form.is_valid():
            form.save()
            messages.success(request, 'Бронирование успешно обновлено!')
            return redirect('my_reservations')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ReservationForm(instance=reservation, room_type=reservation.room_type)

    occupied_reservations = Reservation.objects.filter(
        room_type=reservation.room_type,
        status__in=['pending', 'confirmed', 'checked_in']
    ).exclude(id=reservation.id)  # исключаем текущее бронирование

    occupied_dates = []
    for occ_reservation in occupied_reservations:
        occupied_dates.append({
            'start': occ_reservation.check_in.isoformat(),
            'end': occ_reservation.check_out.isoformat(),
            'text': f"{occ_reservation.check_in.strftime('%d.%m')} - {occ_reservation.check_out.strftime('%d.%m.%Y')}"
        })

    return render(request, 'hotels/edit_reservation.html', {
        'form': form,
        'reservation': reservation,
        'occupied_dates': occupied_dates
    })


@login_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)

    if request.method == 'POST':
        reservation.delete()
        messages.success(request, 'Бронирование успешно удалено!')
        return redirect('my_reservations')

    return render(request, 'hotels/delete_reservation.html', {
        'reservation': reservation
    })


@login_required
def add_review(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)

    # проверяем, не оставлен ли уже отзыв
    if hasattr(reservation, 'review'):
        messages.error(request, 'Вы уже оставили отзыв для этого бронирования.')
        return redirect('my_reservations')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reservation = reservation
            review.save()
            messages.success(request, 'Отзыв успешно добавлен!')
            return redirect('my_reservations')
    else:
        form = ReviewForm()

    return render(request, 'hotels/add_review.html', {
        'form': form,
        'reservation': reservation
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'hotels/register.html', {'form': form})


@staff_member_required
def guest_list(request):
    one_month_ago = timezone.now() - timedelta(days=30)

    # получаем все бронирования за последний месяц с статусом checked_in или checked_out
    recent_reservations = Reservation.objects.filter(
        Q(status='checked_in') | Q(status='checked_out'),
        check_in__gte=one_month_ago.date()
    ).select_related('user', 'room_type', 'room_type__hotel').order_by('-check_in')

    # поиск по имени пользователя или названию отеля
    search_query = request.GET.get('search', '')
    if search_query:
        recent_reservations = recent_reservations.filter(
            Q(user__username__icontains=search_query) |
            Q(room_type__hotel__name__icontains=search_query) |
            Q(room_type__name__icontains=search_query)
        )

    paginator = Paginator(recent_reservations, 10)
    page = request.GET.get('page', 1)

    try:
        reservations = paginator.page(page)
    except PageNotAnInteger:
        reservations = paginator.page(1)
    except EmptyPage:
        reservations = paginator.page(paginator.num_pages)

    return render(request, 'hotels/guest_list.html', {
        'reservations': reservations,
        'search_query': search_query,
        'one_month_ago': one_month_ago.date()
    })