from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Tour, Reservation, Review
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
    return render(request, 'register.html', {'form': form})


def tour_list(request):
    tours = Tour.objects.all()
    return render(request, 'tour_list.html', {'tours': tours})


def tour_detail(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    reviews = Review.objects.filter(tour=tour).order_by('-created_at')
    return render(request, 'tour_detail.html', {'tour': tour, 'reviews': reviews})


@login_required
def reserve_tour(request, pk):
    tour = get_object_or_404(Tour, pk=pk)
    if request.method == 'POST':
        Reservation.objects.create(user=request.user, tour=tour)
        return redirect('my_reservations')
    return render(request, 'reserve_confirm.html', {'tour': tour})


@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_reservations.html', {'reservations': reservations})


@login_required
def edit_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    tours = Tour.objects.all()
    if request.method == 'POST':
        tour_id = request.POST.get('tour')
        reservation.tour = get_object_or_404(Tour, pk=tour_id)
        reservation.save()
        return redirect('my_reservations')
    return render(request, 'edit_reservation.html', {'reservation': reservation, 'tours': tours})


@login_required
def delete_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    if request.method == 'POST':
        reservation.delete()
        return redirect('my_reservations')
    return render(request, 'delete_reservation.html', {'reservation': reservation})


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
    return render(request, 'add_review.html', {'form': form, 'tour': tour})


def sold_tours(request):
    stats = (Reservation.objects
             .filter(status='confirmed')
             .values('tour__country')
             .annotate(count=Count('id'))
             .order_by('tour__country'))
    return render(request, 'sold_tours.html', {'stats': stats})
