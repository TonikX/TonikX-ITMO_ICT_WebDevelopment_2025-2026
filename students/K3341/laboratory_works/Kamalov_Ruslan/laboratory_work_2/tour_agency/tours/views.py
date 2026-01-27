from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.core.paginator import Paginator
from .models import Tour, Reservation, Review, Country
from .forms import RegisterForm, ReservationForm, ReviewForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tour_list')
    else:
        form = RegisterForm()
    return render(request, 'tours/register.html', {'form': form})


def tour_list(request):
    tours = Tour.objects.all()
    
    # Получаем все страны для фильтра
    countries = Country.objects.all()
    
    # Поиск по названию тура
    search_query = request.GET.get('search')
    if search_query:
        tours = tours.filter(name__icontains=search_query)
    
    # Фильтрация по стране
    country_filter = request.GET.get('country')
    if country_filter:
        tours = tours.filter(country_id=country_filter)
    
    # Пагинация
    paginator = Paginator(tours, 5)  # 5 туров на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tours': page_obj,
        'countries': countries,
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': page_obj.has_other_pages(),
    }
    
    return render(request, 'tours/tour_list.html', context)


def tour_detail(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    reviews = tour.reviews.all()
    return render(request, 'tours/tour_detail.html', {'tour': tour, 'reviews': reviews})


@login_required
def reserve_tour(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.tour = tour
            reservation.save()
            messages.success(request, 'Тур зарезервирован!')
            return redirect('my_reservations')
    else:
        form = ReservationForm()
    return render(request, 'tours/reserve_tour.html', {'form': form, 'tour': tour})


@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'tours/my_reservations.html', {'reservations': reservations})


@login_required
def edit_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    if reservation.status == 'confirmed':
        messages.error(request, 'Нельзя редактировать подтвержденное резервирование')
        return redirect('my_reservations')
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('my_reservations')
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'tours/edit_reservation.html', {'form': form})


@login_required
def delete_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    if reservation.status == 'confirmed':
        messages.error(request, 'Нельзя удалить подтвержденное резервирование')
        return redirect('my_reservations')
    if request.method == 'POST':
        reservation.delete()
        return redirect('my_reservations')
    return render(request, 'tours/delete_reservation.html', {'reservation': reservation})


@login_required
def add_review(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.tour = tour
            review.save()
            return redirect('tour_detail', pk=pk)
    else:
        form = ReviewForm()
    return render(request, 'tours/add_review.html', {'form': form, 'tour': tour})


def sales_by_country(request):
    stats = Country.objects.annotate(
        total=Count('tour__reservation', filter=Q(tour__reservation__status='confirmed')),
        people=Sum('tour__reservation__num_people', filter=Q(tour__reservation__status='confirmed'))
    ).filter(total__gt=0)
    return render(request, 'tours/sales_by_country.html', {'stats': stats})
