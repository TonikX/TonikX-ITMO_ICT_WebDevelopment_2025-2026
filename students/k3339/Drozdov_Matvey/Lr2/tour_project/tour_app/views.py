from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import RegisterForm, ReviewForm
from .models import Tour, Reservation, Review
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.contrib.admin.views.decorators import staff_member_required

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("tour_list")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})


def tour_list(request):
    q = request.GET.get("q", "").strip()

    tours_qs = Tour.objects.all().select_related("agency").order_by("id")

    if q:
        tours_qs = tours_qs.filter(
            Q(title__icontains=q) |
            Q(country__icontains=q) |
            Q(agency__name__icontains=q)
        ).distinct()

    paginator = Paginator(tours_qs, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "tour_list.html", {
        "page_obj": page_obj,
        "q": q,
    })


def tour_detail(request, pk):
    tour = get_object_or_404(Tour, pk=pk)

    reservation = None
    user_review = None

    if request.user.is_authenticated:
        reservation = Reservation.objects.filter(user=request.user, tour=tour).first()
        user_review = Review.objects.filter(user=request.user, tour=tour).first()

    # все отзывы по этому туру
    reviews_qs = Review.objects.filter(tour=tour).order_by('-created_at')

    # пагинация отзывов: по 5 на страницу
    page_number = request.GET.get('reviews_page')
    reviews_paginator = Paginator(reviews_qs, 5)
    reviews_page = reviews_paginator.get_page(page_number)

    return render(request, "tour_detail.html", {
        "tour": tour,
        "reservation": reservation,
        "user_review": user_review,
        "reviews_page": reviews_page,
    })


@login_required
def book_tour(request, pk):
    tour = get_object_or_404(Tour, pk=pk)

    # чтобы один и тот же пользователь не бронировал один тур несколько раз
    existing = Reservation.objects.filter(user=request.user, tour=tour).first()
    if existing:
        messages.info(request, "Вы уже бронировали этот тур.")
        return redirect("tour_detail", pk=tour.pk)

    Reservation.objects.create(
        user=request.user,
        tour=tour,
    )

    messages.success(request, "Бронирование оформлено! Ожидает подтверждения администратора.")
    return redirect("tour_detail", pk=tour.pk)


@login_required
def my_reservations(request):
    reservations_qs = Reservation.objects.filter(
        user=request.user
    ).select_related('tour').order_by('-created_at')

    paginator = Paginator(reservations_qs, 5)   # по 5 броней на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "my_reservations.html", {
        "page_obj": page_obj,
    })

@login_required
def cancel_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)

    if request.method == "POST":
        reservation.delete()
        return redirect("my_reservations")

    return render(request, "reservations/cancel_reservation_confirm.html", {
        "reservation": reservation
    })


@login_required
def add_review(request, pk):
    tour = get_object_or_404(Tour, pk=pk)

    # проверяем, что пользователь бронировал этот тур
    has_reservation = Reservation.objects.filter(
        user=request.user,
        tour=tour,
        is_confirmed=True
    ).exists()

    if not has_reservation:
        messages.error(request, "Вы можете оставить отзыв только на забронированные туры.")
        return redirect("tour_detail", pk=tour.pk)

    # проверяем, не оставлял ли уже отзыв
    existing_review = Review.objects.filter(user=request.user, tour=tour).first()
    if existing_review:
        messages.info(request, "Вы уже оставляли отзыв на этот тур.")
        return redirect("tour_detail", pk=tour.pk)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.tour = tour
            review.save()
            messages.success(request, "Отзыв сохранён!")
            return redirect("tour_detail", pk=tour.pk)
    else:
        form = ReviewForm()

    return render(request, "add_review.html", {
        "tour": tour,
        "form": form,
    })


@staff_member_required
def sales_by_country(request):
    stats_qs = (
        Reservation.objects
        .filter(is_confirmed=True)
        .values('tour__country')
        .annotate(total=Count('id'))
        .order_by('tour__country')
    )

    paginator = Paginator(stats_qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "sales_by_country.html", {
        "page_obj": page_obj,
    })



