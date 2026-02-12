from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReservationForm, ReviewForm
from .models import Reservation, Review, Tour


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'tours/registration.html', {'form': form})

@login_required
def home(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'tours/home.html', {'reservations': reservations})

@login_required
def tour_list(request):
    tours = Tour.objects.all()
    return render(request, 'tours/tour_list.html', {'tours': tours})

@login_required
def tour_detail(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    reviews = Review.objects.filter(tour=tour)
    return render(request, 'tours/tour_detail.html', {
        'tour': tour,
        'reviews': reviews,
    })

@login_required
def reserve_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.tour = tour
            reservation.save()
            return redirect('home')
    else:
        form = ReservationForm()

    return render(request, 'tours/reservation_form.html', {'form': form, 'tour': tour})

@login_required
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'tours/reservation_form.html', {'form': form, 'tour': reservation.tour})

@login_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == 'POST':
        reservation.delete()
        return redirect('home')
    return render(request, 'tours/confirm_delete.html', {'reservation': reservation})

@login_required
def submit_review(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.tour = tour
            review.user = request.user 
            review.save()
            return redirect('tour_detail', tour_id=tour.id)
    else:
        form = ReviewForm()
    return render(request, 'tours/review_form.html', {'form': form, 'tour': tour})

@login_required
def sold_tours_by_country(request):
    sold = Reservation.objects.filter(status='подтвержден').values('tour__country').annotate(count=Count('id'))
    return render(request, 'tours/sold_tours_table.html', {'sold': sold})