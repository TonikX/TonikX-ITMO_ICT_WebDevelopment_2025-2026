from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import models
from django.http import HttpRequest, HttpResponse, Http404
from .forms import ReservationForm, CommentForm, RegisterForm, AdminReservationForm, CommentEditForm
from .models import Flight, Reservation, Comment
from .utils import is_airport_admin


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
    Список рейсов с поиском, фильтрами и пагинацией
    '''
    qs = Flight.objects.all()

    # поиск
    q = request.GET.get('q')
    if q:
        qs = qs.filter(
            models.Q(flight_number__icontains=q) | models.Q(airline__icontains=q)
        )

    # фильтры
    flight_type = request.GET.get('type')
    if flight_type in {Flight.FlightType.ARRIVAL, Flight.FlightType.DEPARTURE}:
        qs = qs.filter(flight_type=flight_type)

    date_from = request.GET.get('date_from')
    if date_from:
        qs = qs.filter(departure__date__gte=date_from)

    date_to = request.GET.get('date_to')
    if date_to:
        qs = qs.filter(departure__date__lte=date_to)

    gate = request.GET.get('gate')
    if gate:
        qs = qs.filter(gate__iexact=gate)

    ordering = request.GET.get('ordering') or 'departure'
    qs = qs.order_by(ordering)

    paginator = Paginator(qs, int(request.GET.get('per_page') or 10))
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    ctx = {
        'page_obj': page_obj,
        'request': request,
        'is_admin': is_airport_admin(request.user),
    }
    return render(request, 'flight/flight_list.html', ctx)


@login_required
def create_reservation(request: HttpRequest, flight_id: int) -> HttpResponse:
    '''
    Функция для добавления брони (для обычных пользователей)
    '''
    flight = get_object_or_404(Flight, id=flight_id)

    if request.method == 'POST':
        # Передаем instance с уже установленными полями, чтобы валидация прошла корректно
        form = ReservationForm(request.POST, instance=Reservation(user=request.user, flight=flight, status=Reservation.StatusType.RESERVED))
        if form.is_valid():
            reservation = form.save()
            messages.success(request, 'Бронирование успешно создано.')
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
    reservations = Reservation.objects.filter(flight=flight).select_related('user').order_by('-created_at')
    comments = Comment.objects.filter(flight=flight).select_related('author').order_by('-created_at')

    # Статистика для админа
    reservations_count = reservations.count()
    checked_in_count = reservations.filter(status=Reservation.StatusType.CHECKED_IN).count()

    return render(request, 'flight/flight_detail.html', {
        'flight': flight,
        'reservations': reservations,
        'comments': comments,
        'reservations_count': reservations_count,
        'checked_in_count': checked_in_count,
        'is_admin': is_airport_admin(request.user),
    })


@login_required
def reservation_update(request: HttpRequest, pk: int) -> HttpResponse:
    '''
    Редактирование бронирования
    '''
    reservation = get_object_or_404(Reservation, pk=pk)

    # проверка прав
    if request.user != reservation.user and not is_airport_admin(request.user):
        messages.error(request, 'Вы не можете редактировать это бронирование.')
        return redirect('my_reservations')

    user_is_admin = is_airport_admin(request.user)

    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation, edit_mode=True, is_admin=user_is_admin)
        if form.is_valid():
            form.save()
            messages.success(request, 'Бронирование успешно обновлено.')
            if user_is_admin:
                return redirect('flight_detail', flight_id=reservation.flight.id)
            return redirect('my_reservations')
    else:
        form = ReservationForm(instance=reservation, edit_mode=True, is_admin=user_is_admin)

    return render(request, 'flight/reservation_form.html', {
        'form': form,
        'edit_mode': True,
        'reservation': reservation,
    })


@login_required
def reservation_delete(request: HttpRequest, pk: int) -> HttpResponse:
    '''
    Удаление бронирования
    '''
    reservation = get_object_or_404(Reservation, pk=pk)

    # проверка прав
    if request.user != reservation.user and not is_airport_admin(request.user):
        messages.error(request, 'Вы не можете удалить это бронирование.')
        return redirect('my_reservations')

    if request.method == 'POST':
        flight_id = reservation.flight.id
        reservation.delete()
        messages.success(request, 'Бронирование удалено.')
        if is_airport_admin(request.user):
            return redirect('flight_detail', flight_id=flight_id)
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


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    messages.success(request, 'Вы вышли из аккаунта.')
    return redirect('flight_list')


@login_required
def flight_passengers(request: HttpRequest, flight_id: int) -> HttpResponse:
    '''
    Страница со списком пассажиров рейса (только для администраторов)
    '''
    if not is_airport_admin(request.user):
        raise Http404("Страница не найдена")

    flight = get_object_or_404(Flight, id=flight_id)
    reservations = Reservation.objects.filter(flight=flight).select_related('user').order_by('-updated_at')

    return render(request, 'flight/flight_passengers.html', {
        'flight': flight,
        'reservations': reservations,
    })


@login_required
def admin_create_reservation(request: HttpRequest, flight_id: int) -> HttpResponse:
    '''
    Создание бронирования администратором для любого пользователя
    '''
    if not is_airport_admin(request.user):
        messages.error(request, 'У вас нет прав для выполнения этого действия.')
        return redirect('flight_list')

    flight = get_object_or_404(Flight, id=flight_id)

    if request.method == 'POST':
        form = AdminReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.flight = flight
            reservation.save()
            messages.success(request, f'Бронирование для пользователя {reservation.user.username} успешно создано.')
            return redirect('flight_detail', flight_id=flight.pk)
    else:
        form = AdminReservationForm()

    return render(request, 'flight/admin_reservation_form.html', {
        'form': form,
        'flight': flight,
    })


@login_required
def comment_update(request: HttpRequest, comment_id: int) -> HttpResponse:
    '''
    Редактирование комментария (только для администраторов)
    '''
    comment = get_object_or_404(Comment, id=comment_id)

    # Проверка прав: только админ может редактировать любые комментарии
    if not is_airport_admin(request.user):
        # Обычный пользователь может редактировать только свои комментарии
        if comment.author != request.user:
            messages.error(request, 'Вы не можете редактировать этот комментарий.')
            return redirect('flight_detail', flight_id=comment.flight.id)

    if request.method == 'POST':
        form = CommentEditForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Комментарий успешно обновлен.')
            return redirect('flight_detail', flight_id=comment.flight.id)
    else:
        form = CommentEditForm(instance=comment)

    return render(request, 'flight/comment_edit_form.html', {
        'form': form,
        'comment': comment,
        'flight': comment.flight,
    })


@login_required
def comment_delete(request: HttpRequest, comment_id: int) -> HttpResponse:
    '''
    Удаление комментария (только для администраторов)
    '''
    comment = get_object_or_404(Comment, id=comment_id)

    # Проверка прав: только админ может удалять любые комментарии
    if not is_airport_admin(request.user):
        # Обычный пользователь может удалять только свои комментарии
        if comment.author != request.user:
            messages.error(request, 'Вы не можете удалить этот комментарий.')
            return redirect('flight_detail', flight_id=comment.flight.id)

    if request.method == 'POST':
        flight_id = comment.flight.id
        comment.delete()
        messages.success(request, 'Комментарий удален.')
        return redirect('flight_detail', flight_id=flight_id)

    return render(request, 'flight/comment_confirm_delete.html', {
        'comment': comment,
        'flight': comment.flight,
    })
