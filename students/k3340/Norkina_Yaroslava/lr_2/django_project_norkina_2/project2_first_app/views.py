from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from .models import Trip

from django.views.generic import ListView

class TripListView(ListView):
    model = Trip
    template_name = 'trip_list.html'
    context_object_name = 'trips'  # имя переменной в шаблоне
    paginate_by = 10  # по 10 поездок на страницу

    def get_queryset(self):
        now = timezone.now()
        one_month_ago = now - timedelta(days=30)
        return Trip.objects.filter(
            start_time__gte=one_month_ago
        ).select_related('user', 'car', 'car__model').order_by('-start_time')

from django.contrib.auth import login
from django.urls import reverse_lazy
from .forms import CustomUserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # автоматический вход после регистрации
            return redirect(reverse_lazy('trip_list_last_month'))  # или любой другой маршрут
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


from django.contrib.auth.decorators import login_required
from .models import Trip

@login_required
def user_profile(request):
    """
    Отображает профиль текущего пользователя и его поездки.
    """
    trips = Trip.objects.filter(user=request.user).select_related('car', 'car__model').order_by('-start_time')
    return render(request, 'users/user_profile.html', {
        'user': request.user,
        'trips': trips
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TripForm
from .models import Trip

@login_required
def add_trip(request):
    """Добавить новую поездку"""
    if request.method == 'POST':
        form = TripForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = TripForm(user=request.user)
    return render(request, 'users/add_trip.html', {'form': form})


@login_required
def add_comment(request, trip_id):
    """Добавить комментарий к завершённой поездке (проблемы — только для админа)"""
    trip = get_object_or_404(Trip, pk=trip_id, user=request.user)
    if request.method == 'POST':
        trip.comments = request.POST.get('comments', '').strip()
        trip.save()
        return redirect('user_profile')
    return render(request, 'users/add_comment.html', {'trip': trip})