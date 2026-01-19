from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum
from django.contrib import messages
from .models import Tour, Reservation, Review
from .forms import ReservationForm, ReviewForm, CustomUserCreationForm


def tour_list(request):
    """Список туров с поиском и пагинацией"""
    tours = Tour.objects.all()
    
    # Поиск
    search_query = request.GET.get('search', '')
    if search_query:
        tours = tours.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(travel_agency__icontains=search_query) |
            Q(country__icontains=search_query)
        )
    
    # Пагинация
    paginator = Paginator(tours, 6)  # 6 туров на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'tours/tour_list.html', context)


def tour_detail(request, pk):
    """Детали тура"""
    tour = get_object_or_404(Tour, pk=pk)
    reviews = tour.reviews.all()[:5]  # Последние 5 отзывов
    
    # Проверка, есть ли у пользователя резервирование этого тура
    user_reservation = None
    if request.user.is_authenticated:
        user_reservation = Reservation.objects.filter(tour=tour, user=request.user).first()
    
    context = {
        'tour': tour,
        'reviews': reviews,
        'user_reservation': user_reservation,
    }
    return render(request, 'tours/tour_detail.html', context)


@login_required
def create_reservation(request, tour_id):
    """Создание резервирования тура"""
    tour = get_object_or_404(Tour, pk=tour_id)
    
    # Проверка, есть ли уже резервирование
    existing_reservation = Reservation.objects.filter(tour=tour, user=request.user).first()
    if existing_reservation:
        messages.warning(request, 'У вас уже есть резервирование этого тура.')
        return redirect('tour_detail', pk=tour_id)
    
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.tour = tour
            reservation.user = request.user
            reservation.save()
            messages.success(request, 'Резервирование успешно создано!')
            return redirect('my_reservations')
    else:
        form = ReservationForm()
    
    context = {
        'form': form,
        'tour': tour,
    }
    return render(request, 'tours/create_reservation.html', context)


@login_required
def my_reservations(request):
    """Список резервирований пользователя"""
    reservations = Reservation.objects.filter(user=request.user).order_by('-reservation_date')
    context = {
        'reservations': reservations,
    }
    return render(request, 'tours/my_reservations.html', context)


@login_required
def edit_reservation(request, pk):
    """Редактирование резервирования"""
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    
    if reservation.status == 'confirmed':
        messages.error(request, 'Нельзя редактировать подтвержденное резервирование.')
        return redirect('my_reservations')
    
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Резервирование успешно обновлено!')
            return redirect('my_reservations')
    else:
        form = ReservationForm(instance=reservation)
    
    context = {
        'form': form,
        'reservation': reservation,
    }
    return render(request, 'tours/edit_reservation.html', context)


@login_required
def delete_reservation(request, pk):
    """Удаление резервирования"""
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    
    if reservation.status == 'confirmed':
        messages.error(request, 'Нельзя удалить подтвержденное резервирование.')
        return redirect('my_reservations')
    
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, 'Резервирование успешно удалено!')
        return redirect('my_reservations')
    
    context = {
        'reservation': reservation,
    }
    return render(request, 'tours/delete_reservation.html', context)


@login_required
def create_review(request, tour_id):
    """Создание отзыва о туре"""
    tour = get_object_or_404(Tour, pk=tour_id)
    
    # Проверка, есть ли уже отзыв от этого пользователя
    existing_review = Review.objects.filter(tour=tour, user=request.user).first()
    if existing_review:
        messages.warning(request, 'Вы уже оставили отзыв на этот тур.')
        return redirect('tour_detail', pk=tour_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.tour = tour
            review.user = request.user
            review.save()
            messages.success(request, 'Отзыв успешно добавлен!')
            return redirect('tour_detail', pk=tour_id)
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'tour': tour,
    }
    return render(request, 'tours/create_review.html', context)


def sold_tours_by_country(request):
    """Таблица проданных туров по странам"""
    # Получаем все подтвержденные резервирования
    confirmed_reservations = Reservation.objects.filter(status='confirmed')
    
    # Группируем по странам и считаем количество
    tours_by_country = (
        confirmed_reservations
        .values('tour__country')
        .annotate(
            total_reservations=Count('id'),
            total_tours=Count('tour', distinct=True)
        )
        .order_by('-total_reservations')
    )
    
    context = {
        'tours_by_country': tours_by_country,
    }
    return render(request, 'tours/sold_tours_by_country.html', context)


def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('tour_list')
    else:
        form = CustomUserCreationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'tours/register.html', context)
