from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from shapely import is_valid
from .forms import ReservationForm, CommentForm, RegisterForm
from .models import Flight, Reservation, Comment


def register(request: HttpRequest) -> HttpResponse:
    '''
    Регистрация пользователя
    '''
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('flight_list')
    else:
        form = RegisterForm()
    return render(request, 'flight/register.html', {'form': form})


def flight_list(request: HttpRequest) -> HttpResponse:
    '''
    Список рейсов, отсортированные по времени отправления
    '''
    flights = Flight.objects.all().order_by('departure')
    return render(request, 'flight/flight_list.html', {'flights': flights})


@login_required
def create_reservation(request: HttpRequest, flight_id: int) -> HttpResponse:
    '''
    Функция для добавления брони
    '''
    flight = get_object_or_404(Flight, id=flight_id)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.flight = flight
            reservation.status = Reservation.StatusType.RESERVED
            reservation.save()
            return redirect('flight_detail', flight_id=flight.pk)
        else:
            form = ReservationForm()

    return render(request, 'flight/reservation_form.html', {
        'form': form,
        'flight': flight,
    })


@login_required
def add_comment(request: HttpRequest, flight_id: int) -> HttpResponse:
    '''
    Функция добавления комментариев к рейсу
    '''
    flight = get_object_or_404(Flight, id=flight_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.flight = flight
            comment.flight_date = flight.departure.date()
            comment.save()
            return redirect('flight_detail', flight_id=flight.pk)
        else:
            form = CommentForm()

    return render(request, 'flight/comment_form.html', {
        'form': form,
        'flight': flight,
    })


def flight_detail(request: HttpRequest, flight_id: int) -> HttpResponse:
    '''
    Функция рендера деталей о полёте
    '''
    flight = get_object_or_404(Flight, id=flight_id)
    reservations = Reservation.objects.filter(flight=flight)
    comments = Comment.objects.filter(flight=flight).order_by('-created_at')
    return render(request, 'flight/flight_detail.html', {
        'flight': flight,
        'reservations': reservations,
        'comments': comments,
    })


@login_required
def reservation_update(request: HttpRequest, pk: int) -> HttpResponse:
    '''
    Редактирование бронирования
    '''
    reservation = get_object_or_404(Reservation, pk=pk)

    # проверка прав
    if request.user != reservation.user and not request.user.is_staff:
        messages.error(request, 'Вы не можете редактировать это бронирование.')
        return redirect('my_reservations')

    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Бронирование успешно обновлено.')
            return redirect('my_reservations')
    else:
        form = ReservationForm(instance=reservation)

    return render(request, 'flight/reservation_form.html', {
        'form': form,
        'edit_mode': True,
    })


@login_required
def reservation_delete(request: HttpRequest, pk: int) -> HttpResponse:
    '''
    Удаление бронирования
    '''
    reservation = get_object_or_404(Reservation, pk=pk)

    # проверка прав
    if request.user != reservation.user and not request.user.is_staff:
        messages.error(request, 'Вы не можете удалить это бронирование.')
        return redirect('my_reservations')

    if request.method == 'POST':
        reservation.delete()
        messages.success(request, 'Бронирование удалено.')
        return redirect('my_reservations')

    return render(request, 'flight/reservation_confirm_delete.html', {'reservation': reservation})


@login_required
def my_reservations(request: HttpRequest) -> HttpResponse:
    '''
    Просмотр бронирований авторизованного пользователя + пагинация
    '''
    reservations = Reservation.objects.filter(user=request.user).select_related('flight').order_by('-created_at')

    # пагинация
    pagination = Paginator(reservations, 10)
    page_number = request.GET.get('page')
    page_obj = pagination.get_page(page_number)

    return render(request, 'flight/my_reservations.html', {'page_obj': page_obj})
