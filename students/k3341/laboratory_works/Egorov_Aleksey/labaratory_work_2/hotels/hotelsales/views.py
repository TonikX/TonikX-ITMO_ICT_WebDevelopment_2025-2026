from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from datetime import timedelta
from django.utils import timezone
from django.db.models import Q, Avg
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.db import transaction
from datetime import date
from django.contrib.auth import login
from django.contrib import messages
from .models import Hotel, RoomType, Booking, Review
from .forms import RegisterForm, BookingForm, ReviewForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно! Вы вошли в систему')
            return redirect('hotelsales:home')
    else:
        form = RegisterForm()

    return render(request, "hotelsales/register.html", {"form": form})


def home(request):
    hotels = Hotel.objects.all().order_by('name')

    for hotel in hotels:
        avg_rating = Review.objects.filter(
            booking__room_type__hotel=hotel
        ).aggregate(avg_rating=Avg('rating'))['avg_rating']

        hotel.average_rating = round(avg_rating, 1) if avg_rating is not None else None

    return render(request, 'hotelsales/home.html', {'hotels': hotels})

def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    room_types = hotel.room_type.all().order_by('price_per_night')

    return render(request, 'hotelsales/hotel_detail.html', {
        'hotel': hotel,
        'room_types': room_types,
    })


@login_required
def booking_create(request, room_type_id):
    room_type = get_object_or_404(RoomType, pk=room_type_id)

    if request.method == 'POST':
        form = BookingForm(request.POST, room_type=room_type)
        print("POST данные:", request.POST)
        print("Форма валидна?", form.is_valid())
        if not form.is_valid():
            print("Ошибки:", form.errors.as_text())

        if form.is_valid():
            nights = max((form.cleaned_data['check_out'] - form.cleaned_data['check_in']).days, 1)
            total_price = room_type.price_per_night * nights

            booking = Booking(
                user=request.user,
                room_type=room_type,
                check_in=form.cleaned_data['check_in'],
                check_out=form.cleaned_data['check_out'],
                adults=form.cleaned_data['adults'],
                children=form.cleaned_data['children'],
                status='pending',
                total_price=total_price,
            )

            booking.save()
            print("save прошёл, pk =", booking.pk)

            messages.success(request, f'Бронирование создано! ID = {booking.pk}')
            return redirect('hotelsales:home')

    else:
        form = BookingForm(room_type=room_type)

    return render(request, 'hotelsales/booking_form.html', {
        'form': form,
        'room_type': room_type,
        'hotel': room_type.hotel,
    })

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')

    if request.method == 'POST' and 'cancel_booking' in request.POST:
        booking_id = request.POST.get('booking_id')
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
        if booking.status == 'pending':
            booking.status = 'cancelled'
            booking.save()
            messages.success(request, 'Бронирование отменено.')
        else:
            messages.error(request, 'Это бронирование уже нельзя отменить.')

        return redirect('hotelsales:my_bookings')

    return render(request, 'hotelsales/my_bookings.html', {
        'bookings': bookings,
        'user': request.user,
    })

@login_required
def add_review(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # Можно добавлять отзыв только после выезда или завершения
    if booking.status not in ['checked_out', 'completed']:
        messages.error(request, 'Отзыв можно оставить только после выезда.')
        return redirect('hotelsales:my_bookings')

    if Review.objects.filter(booking=booking).exists():
        messages.error(request, 'Вы уже оставили отзыв на это бронирование.')
        return redirect('hotelsales:my_bookings')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.user = request.user
            review.save()
            messages.success(request, 'Отзыв успешно добавлен!')
            return redirect('hotelsales:my_bookings')
    else:
        form = ReviewForm()

    return render(request, 'hotelsales/add_review.html', {
        'form': form,
        'booking': booking,
    })

@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.status != 'pending':
        messages.error(request, 'Это бронирование уже нельзя редактировать.')
        return redirect('hotelsales:my_bookings')

    if request.method == 'POST':
        form = BookingForm(request.POST, room_type=booking.room_type)
        if form.is_valid():
            booking.check_in = form.cleaned_data['check_in']
            booking.check_out = form.cleaned_data['check_out']
            booking.adults = form.cleaned_data['adults']
            booking.children = form.cleaned_data['children']
            nights = max((booking.check_out - booking.check_in).days, 1)
            booking.total_price = booking.room_type.price_per_night * nights
            booking.save()
            messages.success(request, 'Бронирование обновлено!')
            return redirect('hotelsales:my_bookings')
    else:
        form = BookingForm(initial={
            'check_in': booking.check_in,
            'check_out': booking.check_out,
            'adults': booking.adults,
            'children': booking.children,
        }, room_type=booking.room_type)

    return render(request, 'hotelsales/edit_booking.html', {
        'form': form,
        'booking': booking,
        'hotel': booking.room_type.hotel,
    })

@login_required
def recent_guests(request):
    today = timezone.now().date()
    one_month_ago = today - timedelta(days=30)

    # Гости, которые заселялись или выезжали за последние 30 дней
    recent_bookings = Booking.objects.filter(
        Q(check_in__gte=one_month_ago) | Q(check_out__gte=one_month_ago),
        status__in=['checked_in', 'checked_out', 'completed']
    ).order_by('-check_in')

    return render(request, 'hotelsales/recent_guests.html', {
        'bookings': recent_bookings,
        'period_start': one_month_ago,
        'period_end': today,
    })