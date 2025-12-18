from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from .models import Tour, Reservation, Review
from .forms import ReservationForm, ReviewForm, UserRegistrationForm, UserLoginForm


def tour_list(request):
    tours = Tour.objects.all()
    
    # Поиск по названию, стране или агентству
    search_query = request.GET.get('search')
    if search_query:
        tours = tours.filter(
            Q(title__icontains=search_query) |
            Q(country__icontains=search_query) |
            Q(agency__icontains=search_query)
        )
    
    # Пагинация: 6 туров на страницу
    paginator = Paginator(tours, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'tourism/tour_list.html', context)


def tour_detail(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    reviews = Review.objects.filter(tour=tour).order_by('-created_at')
    
    # Пагинация отзывов: 5 на страницу
    paginator = Paginator(reviews, 5)
    page_number = request.GET.get('page')
    reviews_page = paginator.get_page(page_number)
    
    context = {
        'tour': tour,
        'reviews_page': reviews_page,
    }
    return render(request, 'tourism/tour_detail.html', context)


@login_required
def make_reservation(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.tour = tour
            reservation.user = request.user
            
            # Проверка доступности мест: считаем участников из pending и confirmed резервирований
            total_reserved = Reservation.objects.filter(
                tour=tour, 
                status__in=['pending', 'confirmed']
            ).aggregate(total=Sum('participants_count'))['total'] or 0
            
            if total_reserved + reservation.participants_count <= tour.max_participants:
                reservation.save()
                messages.success(request, 'Резервирование успешно создано!')
                return redirect('tourism:my_reservations')
            else:
                messages.error(request, 'Недостаточно мест для данного количества участников.')
    else:
        form = ReservationForm()
    
    context = {
        'tour': tour,
        'form': form,
    }
    return render(request, 'tourism/make_reservation.html', context)


@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user).order_by('-created_at')
    
    paginator = Paginator(reservations, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'tourism/my_reservations.html', context)


@login_required
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Резервирование успешно обновлено!')
            return redirect('tourism:my_reservations')
    else:
        form = ReservationForm(instance=reservation)
    
    context = {
        'form': form,
        'reservation': reservation,
    }
    return render(request, 'tourism/edit_reservation.html', context)


@login_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, 'Резервирование успешно удалено!')
        return redirect('tourism:my_reservations')
    
    context = {
        'reservation': reservation,
    }
    return render(request, 'tourism/delete_reservation.html', context)


@login_required
def add_review(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.tour = tour
            review.user = request.user
            review.save()
            messages.success(request, 'Отзыв успешно добавлен!')
            return redirect('tourism:tour_detail', tour_id=tour.id)
    else:
        form = ReviewForm()
    
    context = {
        'tour': tour,
        'form': form,
    }
    return render(request, 'tourism/add_review.html', context)


def tours_by_country(request):
    # Фильтрация проданных туров (только с confirmed резервированиями), группировка по странам и подсчет
    tours = Tour.objects.filter(
        reservation__status='confirmed'
    ).values('country').annotate(
        total_tours=Count('id')
    ).order_by('country')
    
    context = {
        'tours_by_country': tours,
    }
    return render(request, 'tourism/tours_by_country.html', context)


@login_required
def reservations_by_country(request, country):
    if not request.user.is_staff:
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('tourism:tour_list')
    
    reservations = Reservation.objects.filter(
        tour__country=country,
        status='confirmed'
    ).order_by('-created_at')
    
    paginator = Paginator(reservations, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'country': country,
        'page_obj': page_obj,
    }
    return render(request, 'tourism/reservations_by_country.html', context)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('tourism:tour_list')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}! Регистрация прошла успешно.')
            return redirect('tourism:tour_list')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'tourism/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('tourism:tour_list')
    
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('tourism:tour_list')
    else:
        form = UserLoginForm()
    
    return render(request, 'tourism/login.html', {'form': form})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('tourism:tour_list')


@login_required
def admin_reservations(request):
    if not request.user.is_staff:
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('tourism:tour_list')
    
    reservations = Reservation.objects.all().order_by('-created_at')
    
    # Фильтрация по статусу резервирования
    status_filter = request.GET.get('status')
    if status_filter:
        reservations = reservations.filter(status=status_filter)
    
    # Пагинация: 20 резервирований на страницу
    paginator = Paginator(reservations, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'status_choices': Reservation.STATUS_CHOICES,
    }
    return render(request, 'tourism/admin_reservations.html', context)


@login_required
def confirm_reservation(request, reservation_id):
    if not request.user.is_staff:
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('tourism:tour_list')
    
    reservation = get_object_or_404(Reservation, id=reservation_id)
    
    if request.method == 'POST':
        reservation.status = 'confirmed'
        reservation.save()
        messages.success(request, f'Резервирование от {reservation.user.username} для тура "{reservation.tour.title}" подтверждено.')
        return redirect('tourism:admin_reservations')
    
    return redirect('tourism:admin_reservations')


@login_required
def cancel_reservation_admin(request, reservation_id):
    if not request.user.is_staff:
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('tourism:tour_list')
    
    reservation = get_object_or_404(Reservation, id=reservation_id)
    
    if request.method == 'POST':
        reservation.status = 'cancelled'
        reservation.save()
        messages.success(request, f'Резервирование от {reservation.user.username} для тура "{reservation.tour.title}" отменено.')
        return redirect('tourism:admin_reservations')
    
    return redirect('tourism:admin_reservations')
