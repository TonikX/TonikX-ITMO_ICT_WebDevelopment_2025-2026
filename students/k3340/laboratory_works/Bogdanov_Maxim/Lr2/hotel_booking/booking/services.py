from django.db.models import Q
from datetime import date, timedelta
from .models import Booking, Room


def check_room_availability(room, check_in, check_out, exclude_booking_id=None):
    """
    Проверяет доступность номера на указанные даты.
    Возвращает True, если номер доступен, иначе False.
    """
    blocking_statuses = ['confirmed', 'checked_in', 'checked_out']

    overlapping_bookings = Booking.objects.filter(
        room=room,
        status__in=blocking_statuses
    ).filter(
        # Пересечение интервалов: NOT (booking.check_out <= check_in OR booking.check_in >= check_out)
        ~Q(check_out__lte=check_in) & ~Q(check_in__gte=check_out)
    )

    if exclude_booking_id:
        overlapping_bookings = overlapping_bookings.exclude(id=exclude_booking_id)

    return not overlapping_bookings.exists()


def get_available_rooms(check_in, check_out, hotel=None, room_type=None):
    """
    Возвращает QuerySet доступных номеров на указанные даты.
    """
    rooms = Room.objects.filter(is_active=True).select_related('room_type__hotel')

    if hotel:
        rooms = rooms.filter(room_type__hotel=hotel)

    if room_type:
        rooms = rooms.filter(room_type=room_type)

    # Получаем ID номеров с пересекающимися бронированиями
    blocking_statuses = ['confirmed', 'checked_in', 'checked_out']
    unavailable_room_ids = Booking.objects.filter(
        status__in=blocking_statuses
    ).filter(
        ~Q(check_out__lte=check_in) & ~Q(check_in__gte=check_out)
    ).values_list('room_id', flat=True)

    # Исключаем недоступные номера
    return rooms.exclude(id__in=unavailable_room_ids)


def get_recent_guests(hotel, days=30):
    """
    Возвращает постояльцев отеля за последние N дней.
    """
    cutoff_date = date.today() - timedelta(days=days)

    bookings = Booking.objects.filter(
        room__room_type__hotel=hotel,
        check_in__lte=date.today(),
        check_out__gte=cutoff_date,
        status__in=['checked_in', 'checked_out']
    ).select_related('user', 'room__room_type').order_by('-check_in')

    return bookings


def calculate_booking_price(room, check_in, check_out):
    """
    Рассчитывает стоимость бронирования.
    """
    nights = (check_out - check_in).days
    return room.room_type.price_per_night * nights


def can_check_in(booking):
    """
    Проверяет возможность заселения (переход confirmed -> checked_in).
    """
    return (
            booking.status == 'confirmed' and
            booking.check_in <= date.today()
    )


def can_check_out(booking):
    """
    Проверяет возможность выселения (переход checked_in -> checked_out).
    """
    return booking.status == 'checked_in'