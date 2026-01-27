from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from django.db.models import Q
from .models import Flight, Reservation, Review
from .forms import UserRegistrationForm, ReservationForm, ReviewForm


class FlightListView(ListView):
    """Список рейсов с пагинацией и поиском"""
    model = Flight
    template_name = 'flights/flight_list.html'
    context_object_name = 'flights'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Flight.objects.all()
        search_query = self.request.GET.get('search', '')
        
        if search_query:
            queryset = queryset.filter(
                Q(flight_number__icontains=search_query) |
                Q(airline__icontains=search_query) |
                Q(gate_number__icontains=search_query)
            )
        
        return queryset.order_by('departure_time')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context


def register_view(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('flight_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'flights/register.html', {'form': form})


@login_required
def flight_detail(request, pk):
    """Детальная информация о рейсе"""
    flight = get_object_or_404(Flight, pk=pk)
    reservations = Reservation.objects.filter(flight=flight, status='confirmed')
    reviews = Review.objects.filter(flight=flight)
    user_reservation = None
    
    if request.user.is_authenticated:
        user_reservation = Reservation.objects.filter(flight=flight, user=request.user).first()
    
    context = {
        'flight': flight,
        'reservations': reservations,
        'reviews': reviews,
        'user_reservation': user_reservation,
        'available_seats': flight.available_seats(),
    }
    return render(request, 'flights/flight_detail.html', context)


@login_required
def create_reservation(request, flight_id):
    """Создание резервирования места"""
    flight = get_object_or_404(Flight, pk=flight_id)
    
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.flight = flight
            
            # Проверка, не занято ли место
            if Reservation.objects.filter(flight=flight, seat_number=reservation.seat_number, status='confirmed').exists():
                messages.error(request, 'Это место уже занято!')
                return redirect('flight_detail', pk=flight_id)
            
            reservation.save()
            messages.success(request, f'Место {reservation.seat_number} успешно зарезервировано!')
            return redirect('flight_detail', pk=flight_id)
    else:
        form = ReservationForm()
    
    return render(request, 'flights/create_reservation.html', {
        'form': form,
        'flight': flight
    })


@login_required
def edit_reservation(request, reservation_id):
    """Редактирование резервирования"""
    reservation = get_object_or_404(Reservation, pk=reservation_id, user=request.user)
    
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            # Проверка, не занято ли новое место
            new_seat = form.cleaned_data['seat_number']
            if Reservation.objects.filter(
                flight=reservation.flight,
                seat_number=new_seat,
                status='confirmed'
            ).exclude(pk=reservation_id).exists():
                messages.error(request, 'Это место уже занято!')
                return redirect('edit_reservation', reservation_id=reservation_id)
            
            form.save()
            messages.success(request, 'Резервирование успешно обновлено!')
            return redirect('my_reservations')
    else:
        form = ReservationForm(instance=reservation)
    
    return render(request, 'flights/edit_reservation.html', {
        'form': form,
        'reservation': reservation
    })


@login_required
def delete_reservation(request, reservation_id):
    """Удаление резервирования"""
    reservation = get_object_or_404(Reservation, pk=reservation_id, user=request.user)
    
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, 'Резервирование успешно удалено!')
        return redirect('my_reservations')
    
    return render(request, 'flights/delete_reservation.html', {
        'reservation': reservation
    })


@login_required
def my_reservations(request):
    """Список резервирований пользователя"""
    reservations = Reservation.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'flights/my_reservations.html', {
        'reservations': reservations
    })


@login_required
def create_review(request, flight_id):
    """Создание отзыва о рейсе"""
    flight = get_object_or_404(Flight, pk=flight_id)
    
    # Проверка, не оставлял ли пользователь уже отзыв
    if Review.objects.filter(flight=flight, user=request.user).exists():
        messages.error(request, 'Вы уже оставили отзыв на этот рейс!')
        return redirect('flight_detail', pk=flight_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.flight = flight
            review.save()
            messages.success(request, 'Отзыв успешно добавлен!')
            return redirect('flight_detail', pk=flight_id)
    else:
        form = ReviewForm()
    
    return render(request, 'flights/create_review.html', {
        'form': form,
        'flight': flight
    })


@login_required
def flight_passengers(request, flight_id):
    """Таблица пассажиров рейса"""
    flight = get_object_or_404(Flight, pk=flight_id)
    reservations = Reservation.objects.filter(flight=flight, status='confirmed').select_related('user', 'ticket')
    
    passengers = []
    for reservation in reservations:
        passenger_info = {
            'reservation': reservation,
            'user': reservation.user,
            'seat_number': reservation.seat_number,
            'ticket': getattr(reservation, 'ticket', None),
        }
        passengers.append(passenger_info)



    return render(request, 'flights/flight_passengers.html', {
        'flight': flight,
        'passengers': passengers
    })

