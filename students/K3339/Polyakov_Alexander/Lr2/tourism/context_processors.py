from .models import Reservation


def pending_reservations_count(request):
    if request.user.is_authenticated and request.user.is_staff:
        return {
            'pending_reservations_count': Reservation.objects.filter(status='pending').count()
        }
    return {'pending_reservations_count': 0}
