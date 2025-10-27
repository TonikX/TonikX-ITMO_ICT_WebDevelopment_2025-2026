from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from .models import Hotel, RoomType, Reservation, Review
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserLoginForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserRegisterForm


def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Автоматически входим после регистрации
            login(request, user)

            # Сообщение об успехе
            messages.success(request, f'Аккаунт создан для {user.username}! Добро пожаловать!')
            return redirect('hotel_list')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = UserRegisterForm()

    return render(request, 'hotels/register.html', {'form': form})

def user_login(request):
    """Вход для обычных пользователей (не требует is_staff)"""
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('hotel_list')
    else:
        form = UserLoginForm()

    return render(request, 'hotels/login.html', {'form': form})


def user_logout(request):
    """Выход пользователя"""
    logout(request)
    return redirect('hotel_list')


@login_required
def profile(request):
    """Профиль пользователя"""
    return render(request, 'hotels/profile.html', {'user': request.user})

class HotelListView(ListView):
    model = Hotel
    template_name = 'hotels/hotel_list.html'
    context_object_name = 'hotels'
    paginate_by = 5  # Количество отелей на странице

    def get_queryset(self):
        # Получаем базовый запрос
        queryset = Hotel.objects.all()

        # Обработка поискового запроса
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(address__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Сохраняем поисковый запрос для пагинации
        context['search_query'] = self.request.GET.get('q', '')
        return context


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render


'''def hotel_search(request):
    hotel_list = Hotel.objects.all()
    search_query = request.GET.get('q')

    if search_query:
        hotel_list = hotel_list.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    paginator = Paginator(hotel_list, 5)  # 5 отелей на странице
    page = request.GET.get('page')

    try:
        hotels = paginator.page(page)
    except PageNotAnInteger:
        hotels = paginator.page(1)
    except EmptyPage:
        hotels = paginator.page(paginator.num_pages)

    context = {
        'hotels': hotels,
        'search_query': search_query or ''
    }
    return render(request, 'hotels/hotel_list.html', context)'''


from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import ReservationForm  # Добавь этот импорт
from django.urls import reverse_lazy


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm  # Используем нашу форму
    template_name = 'hotels/reservation_form.html'
    success_url = reverse_lazy('user_reservations')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

from django.core.exceptions import PermissionDenied

class AllReservationsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Просмотр всех бронирований - только для администраторов"""
    model = Reservation
    template_name = 'hotels/all_reservations.html'
    context_object_name = 'reservations'
    paginate_by = 10

    def test_func(self):
        # Только staff пользователи (администраторы) имеют доступ
        return self.request.user.is_staff

    def get_queryset(self):
        return Reservation.objects.all().order_by('-created_at')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied("У вас нет прав для просмотра этой страницы")
        return super().dispatch(request, *args, **kwargs)


class UserReservationListView(LoginRequiredMixin, ListView):
    """
    Список бронирований текущего пользователя
    """
    model = Reservation
    template_name = 'hotels/user_reservations.html'
    context_object_name = 'reservations'
    paginate_by = 5

    def get_queryset(self):
        # Показываем только бронирования текущего пользователя
        return Reservation.objects.filter(user=self.request.user).order_by('-created_at')

class ReservationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Reservation
    form_class = ReservationForm  # Используем нашу форму
    template_name = 'hotels/reservation_form.html'
    success_url = reverse_lazy('user_reservations')

    def test_func(self):
        reservation = self.get_object()
        return self.request.user == reservation.user

class ReservationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Reservation
    template_name = 'hotels/reservation_confirm_delete.html'
    success_url = reverse_lazy('user_reservations')

    def test_func(self):
        reservation = self.get_object()
        return self.request.user == reservation.user


from .forms import ReviewForm  # Добавь этот импорт


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'hotels/review_form.html'
    success_url = reverse_lazy('review_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReviewListView(ListView):
    model = Review
    template_name = 'hotels/review_list.html'
    context_object_name = 'reviews'
    paginate_by = 10
    ordering = ['-created_at']


class UserReviewListView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'hotels/user_reviews.html'
    context_object_name = 'reviews'
    paginate_by = 10

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user).order_by('-created_at')


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'hotels/review_confirm_delete.html'
    success_url = reverse_lazy('user_reviews')

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.user


from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def guest_report(request):
    """Отчет по постояльцам - только для администраторов"""
    # Вычисляем дату 30 дней назад
    last_month = timezone.now().date() - timedelta(days=30)

    # Получаем все бронирования за последний месяц
    reservations = Reservation.objects.filter(
        check_in__gte=last_month
    ).select_related('user', 'room_type__hotel').order_by('-check_in')

    # Группируем по отелям для статистики
    hotel_stats = {}
    for reservation in reservations:
        hotel_name = reservation.room_type.hotel.name
        if hotel_name not in hotel_stats:
            hotel_stats[hotel_name] = {
                'total_guests': 0,
                'reservations': []
            }
        hotel_stats[hotel_name]['total_guests'] += 1
        hotel_stats[hotel_name]['reservations'].append(reservation)

    context = {
        'reservations': reservations,
        'hotel_stats': hotel_stats,
        'period_start': last_month,
        'period_end': timezone.now().date()
    }
    return render(request, 'hotels/guest_report.html', context)



def home_page(request):
    """
    Главная страница сайта
    """
    return render(request, 'hotels/home.html')