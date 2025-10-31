from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q, Avg
from .models import Flight, Reservation, Review
from .forms import (
    UserRegistrationForm, UserLoginForm, FlightSearchForm,
    ReservationForm, ReviewForm
)


def home(request):
    """главная страница с поиском рейсов"""
    form = FlightSearchForm(request.GET or None)
    flights = Flight.objects.all()
    
    if form.is_valid():
        departure_city = form.cleaned_data.get('departure_city')
        arrival_city = form.cleaned_data.get('arrival_city')
        departure_date = form.cleaned_data.get('departure_date')
        flight_type = form.cleaned_data.get('flight_type')
        
        if departure_city:
            flights = flights.filter(departure_city__icontains=departure_city)
        if arrival_city:
            flights = flights.filter(arrival_city__icontains=arrival_city)
        if departure_date:
            flights = flights.filter(departure_time__date=departure_date)
        if flight_type:
            flights = flights.filter(flight_type=flight_type)
    
    # добавляем аннотацию со средним рейтингом
    flights = flights.annotate(avg_rating=Avg('reviews__rating'))
    
    context = {
        'form': form,
        'flights': flights,
    }
    return render(request, 'home.html', context)


def register_view(request):
    """регистрация нового пользователя"""
    if request.user.is_authenticated:
        return redirect('flight_list')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно! Добро пожаловать!')
            return redirect('flight_list')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    """вход пользователя"""
    if request.user.is_authenticated:
        return redirect('flight_list')
    
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('flight_list')
    else:
        form = UserLoginForm()
    
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    """выход пользователя"""
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы')
    return redirect('home')


class FlightListView(ListView):
    """список всех рейсов"""
    model = Flight
    template_name = 'flights/flight_list.html'
    context_object_name = 'flights'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Flight.objects.all().annotate(avg_rating=Avg('reviews__rating'))
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(flight_number__icontains=search) |
                Q(airline__icontains=search) |
                Q(departure_city__icontains=search) |
                Q(arrival_city__icontains=search)
            )
        return queryset


class FlightDetailView(DetailView):
    """детальная информация о рейсе"""
    model = Flight
    template_name = 'flights/flight_detail.html'
    context_object_name = 'flight'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        flight = self.get_object()
        
        # проверяем, есть ли у пользователя резервирование на этот рейс
        if self.request.user.is_authenticated:
            context['user_reservation'] = Reservation.objects.filter(
                user=self.request.user,
                flight=flight
            ).first()
        
        # получаем все резервирования для отображения пассажиров
        context['reservations'] = flight.reservations.filter(
            is_confirmed=True
        ).select_related('user')
        
        # получаем отзывы
        context['reviews'] = flight.reviews.all().select_related('user')
        context['avg_rating'] = flight.reviews.aggregate(Avg('rating'))['rating__avg']
        
        return context


@login_required
def create_reservation(request, flight_id):
    """создание резервирования"""
    flight = get_object_or_404(Flight, pk=flight_id)
    
    # проверяем, нет ли уже резервирования у пользователя на этот рейс
    existing_reservation = Reservation.objects.filter(
        user=request.user,
        flight=flight
    ).first()
    
    if existing_reservation:
        messages.warning(request, 'У вас уже есть резервирование на этот рейс!')
        return redirect('flight_detail', pk=flight_id)
    
    # проверяем доступность мест
    if not flight.is_available:
        messages.error(request, 'К сожалению, на этом рейсе нет свободных мест')
        return redirect('flight_detail', pk=flight_id)
    
    if request.method == 'POST':
        form = ReservationForm(request.POST, user=request.user, flight=flight)
        if form.is_valid():
            reservation = form.save()
            messages.success(request, 'Резервирование создано успешно! Ожидайте подтверждения администратора.')
            return redirect('my_reservations')
    else:
        form = ReservationForm(user=request.user, flight=flight)
    
    return render(request, 'reservations/create_reservation.html', {
        'form': form,
        'flight': flight
    })


@login_required
def my_reservations(request):
    """мои резервирования"""
    reservations = Reservation.objects.filter(
        user=request.user
    ).select_related('flight').order_by('-created_at')
    
    return render(request, 'reservations/my_reservations.html', {
        'reservations': reservations
    })


@login_required
def cancel_reservation(request, reservation_id):
    """отмена резервирования"""
    reservation = get_object_or_404(
        Reservation,
        pk=reservation_id,
        user=request.user
    )
    
    if request.method == 'POST':
        reservation.status = 'cancelled'
        reservation.save()
        messages.success(request, 'Резервирование отменено')
        return redirect('my_reservations')
    
    return render(request, 'reservations/cancel_reservation.html', {
        'reservation': reservation
    })


@login_required
def create_review(request, flight_id):
    """создание отзыва"""
    flight = get_object_or_404(Flight, pk=flight_id)
    
    # проверяем, нет ли уже отзыва от этого пользователя
    existing_review = Review.objects.filter(
        user=request.user,
        flight=flight
    ).first()
    
    if existing_review:
        messages.warning(request, 'Вы уже оставили отзыв на этот рейс!')
        return redirect('flight_detail', pk=flight_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, user=request.user, flight=flight)
        if form.is_valid():
            review = form.save()
            messages.success(request, 'Спасибо за ваш отзыв!')
            return redirect('flight_detail', pk=flight_id)
    else:
        form = ReviewForm(user=request.user, flight=flight)
    
    return render(request, 'reviews/create_review.html', {
        'form': form,
        'flight': flight
    })


@login_required
def my_reviews(request):
    """мои отзывы"""
    reviews = Review.objects.filter(
        user=request.user
    ).select_related('flight').order_by('-created_at')
    
    return render(request, 'reviews/my_reviews.html', {
        'reviews': reviews
    })


@login_required
def delete_review(request, review_id):
    """удаление отзыва"""
    review = get_object_or_404(
        Review,
        pk=review_id,
        user=request.user
    )
    
    if request.method == 'POST':
        flight_id = review.flight.id
        review.delete()
        messages.success(request, 'Отзыв удален')
        return redirect('flight_detail', pk=flight_id)
    
    return render(request, 'reviews/delete_review.html', {
        'review': review
    })
