from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from main.forms import TourForm, ReviewForm
from main.models import Tour, Reservation, Review


def tour_list(request):
    """Функция для отображения всех туров"""

    tours = Tour.objects.all()
    return render(request, 'main/tour_list.html', {'tours': tours})

def tour_detail(request, pk):
    """Функция для страницы тура"""

    tour = get_object_or_404(Tour, pk=pk)
    reservation = None
    reserved = False

    # Проверка на авторизованность у пользователя
    if request.user.is_authenticated:
        reservation = Reservation.objects.filter(user=request.user, tour=tour)
        reserved = reservation is not None

    reviews = Review.objects.filter(tour=tour).select_related('user').order_by('-tour_date')

    return render(request, 'main/tour_detail.html', {
        'tour': tour,
        'reserved': reserved,
        'reservation': reservation,
        'reviews': reviews,
    })

@login_required
def reserve_tour(request, pk):
    """Метод для резервирования тура. Только для авторизированных пользователей."""

    tour = get_object_or_404(Tour, pk=pk)
    active_statuses = ['waiting', 'approved']
    existing = Reservation.objects.filter(user=request.user, tour=tour, status__in=active_statuses).exists()
    if not existing and request.method == "POST":
        Reservation.objects.create(user=request.user, tour=tour, status='waiting')
    return redirect('tour_detail', pk=pk)

@login_required
def cancel_reservation(request, pk):
    """Метод для отмены резервирования тура. Только для авторизированных пользователей."""
    tour = get_object_or_404(Tour, pk=pk)
    Reservation.objects.filter(user=request.user, tour=tour).delete()
    return redirect('tour_detail', pk=pk)

def is_admin(user):
    """Метод для определения группы пользователя."""

    return user.groups.filter(name='Администратор').exists() or user.is_staff

@user_passes_test(is_admin)
def create_tour(request):
    """Метод для создания тура. Только для администраторов."""

    if request.method == 'POST':
        form = TourForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tour_list')
    else:
        form = TourForm()
    return render(request, 'main/tour_form.html', {'form': form})

@user_passes_test(is_admin)
def edit_tour(request, pk):
    """Метод для редактирования тура. Только для администраторов."""

    tour = get_object_or_404(Tour, pk=pk)
    if request.method == 'POST':
        form = TourForm(request.POST, instance=tour)
        if form.is_valid():
            form.save()
            return redirect('tour_detail', pk=pk)
    else:
        form = TourForm(instance=tour)
    return render(request, 'main/tour_form.html', {'form': form})

@user_passes_test(is_admin)
def delete_tour(request, pk):
    """Метод для удаления тура. Только для администраторов."""

    tour = get_object_or_404(Tour, pk=pk)
    if request.method == 'POST':
        tour.delete()
        return redirect('tour_list')
    return render(request, 'main/tour_delete.html', {'tour': tour})

@user_passes_test(is_admin)
def reservations_admin(request):
    """Отображение всех резерваций пользователей"""

    reservations = Reservation.objects.select_related('user', 'tour').order_by('-reserved_at')
    return render(request, 'main/reservations_admin.html', {'reservations': reservations})

@user_passes_test(is_admin)
def approve_reservation(request, pk):
    """Метод подтверждения резервации"""

    reservation = get_object_or_404(Reservation, pk=pk)
    reservation.status = 'approved'
    reservation.save()
    return redirect('reservations_admin')

@user_passes_test(is_admin)
def refuse_reservation(request, pk):
    """Метод для отклонения резервирования"""

    reservation = get_object_or_404(Reservation, pk=pk)
    reservation.status = 'refused'
    reservation.save()
    return redirect('reservations_admin')



@login_required
def add_review(request, tour_pk):
    """Метод для создания отзыва"""

    tour = get_object_or_404(Tour, pk=tour_pk)
    if request.user.is_staff or request.user.groups.filter(name='Администратор').exists():
        return redirect('tour_detail', pk=tour_pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.tour = tour
            review.user = request.user
            review.save()
            return redirect('tour_detail', pk=tour_pk)
    else:
        form = ReviewForm()
    return render(request, 'main/review_form.html', {'form': form, 'tour': tour})

@login_required
def edit_review(request, pk):
    """Метод для редактирования отзыва"""

    review = get_object_or_404(Review, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('tour_detail', pk=review.tour.pk)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'main/review_form.html', {'form': form, 'tour': review.tour})

@login_required
def delete_review(request, pk):
    """Метод для удаления отзыва"""

    review = get_object_or_404(Review, pk=pk, user=request.user)
    tour_pk = review.tour.pk
    if request.method == 'POST':
        review.delete()
        return redirect('tour_detail', pk=tour_pk)
    return render(request, 'main/review_confirm_delete.html', {'review': review})