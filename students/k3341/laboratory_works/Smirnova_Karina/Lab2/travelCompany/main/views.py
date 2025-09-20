from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from main.forms import TourForm
from main.models import Tour, Reservation


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
        reservation = Reservation.objects.filter(user=request.user, tour=tour).first()
        reserved = reservation is not None
    return render(request, 'main/tour_detail.html', {
        'tour': tour,
        'reserved': reserved,
        'reservation': reservation,
    })

@login_required
def reserve_tour(request, pk):
    """Метод для резервирования тура. Только для авторизированных пользователей."""

    tour = get_object_or_404(Tour, pk=pk)
    if not Reservation.objects.filter(user=request.user, tour=tour).exists():
        Reservation.objects.create(user=request.user, tour=tour, reserved_at=timezone.now())
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