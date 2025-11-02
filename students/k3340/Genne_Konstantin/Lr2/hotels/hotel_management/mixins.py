from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect

class ReviewAllowedMixin(UserPassesTestMixin):    
    def test_func(self):
        reservation_id = self.kwargs.get('reservation_id')
        from .models import Reservation
        reservation = Reservation.objects.get(id=reservation_id)
        
        return (reservation.user == self.request.user and 
                reservation.status == 'checked_out' and 
                not hasattr(reservation, 'review'))
    
    def handle_no_permission(self):
        messages.error(self.request, "Вы не можете оставить отзыв для этого бронирования.")
        return redirect('my_reservations')
    
class ReservationEditableMixin(UserPassesTestMixin):    
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user and obj.status in ['pending', 'confirmed']
    
    def handle_no_permission(self):
        obj = self.get_object()
        if self.request.user != obj.user:
            messages.error(self.request, "У вас нет прав для выполнения этого действия.")
        else:
            messages.error(self.request, "Это бронирование нельзя редактировать (возможно, оно уже заселено или отменено).")
        return redirect('my_reservations')