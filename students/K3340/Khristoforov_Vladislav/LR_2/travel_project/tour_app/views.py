from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .decorators import staff_required
from django.db.models import Count, Q, Avg, Sum, F
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.contrib import messages
from .filters import TourFilter, BookingFilter
from .models import Tour, Booking, Review
from .forms import BookingForm, ReviewForm, TourForm

class TourListView(ListView):
    model = Tour
    template_name = 'tour_app/tour_list.html'
    context_object_name = 'tours'
    paginate_by = 6

    def get_queryset(self):
        # Показываем только активные туры
        queryset = Tour.objects.filter(end_date__gte=timezone.now().date()).order_by('start_date')
        self.filterset = TourFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        
        filters_config = [
            {'key': 'search', 'label': 'Поиск', 'format': '"{value}"', 'remove_url': self._build_remove_url('search')},
            {'key': 'country', 'label': 'Страна', 'format': '"{value}"', 'remove_url': self._build_remove_url('country')},
            {'key': 'min_price', 'label': 'Цена от', 'format': '{value} руб.', 'remove_url': self._build_remove_url('min_price')},
            {'key': 'max_price', 'label': 'Цена до', 'format': '{value} руб.', 'remove_url': self._build_remove_url('max_price')},
        ]

        active_filters = []
        for config in filters_config:
            value = self.request.GET.get(config['key'])
            if value:
                config['value'] = value
                config['display_value'] = config['format'].format(value=value)
                active_filters.append(config)

        context['active_filters'] = active_filters
        return context

    def _build_remove_url(self, exclude_param):
        params = []
        for key, value in self.request.GET.items():
            if key != exclude_param and key != 'page':
                params.append(f"{key}={value}")
        return "?" + "&".join(params) if params else "?"

class TourDetailView(DetailView):
    model = Tour
    template_name = 'tour_app/tour_detail.html'
    context_object_name = 'tour'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tour = self.get_object()
        context['reviews'] = Review.objects.filter(tour=tour)
        context['booking_form'] = BookingForm()
        context['review_form'] = ReviewForm()
        context['is_archive'] = tour.end_date < timezone.now().date()
       
        return context

    def post(self, request, *args, **kwargs):
        tour = self.get_object()

        if 'booking' in request.POST and request.user.is_authenticated:
            booking_form = BookingForm(request.POST)
            if booking_form.is_valid():
                booking = booking_form.save(commit=False)
                booking.user = request.user
                booking.tour = tour
                
                # Проверяем доступность мест
                if not tour.can_book(booking.persons):
                    messages.error(request, 
                        f'Недостаточно свободных мест. Доступно: {tour.get_available_spots()}')
                    return self.get(request, *args, **kwargs)
                
                booking.save()
                messages.success(request, 'Тур успешно забронирован! Ожидайте подтверждения.')
                return redirect('my_bookings')
            else:
                messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')

        elif 'review' in request.POST and request.user.is_authenticated:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.tour = tour
                review.save()
                messages.success(request, 'Отзыв успешно добавлен!')
                return redirect('tour_detail', pk=tour.id)
            else:
                messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')

        return self.get(request, *args, **kwargs)

class MyBookingsListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'tour_app/my_bookings.html'
    context_object_name = 'bookings'
    paginate_by = 10

    def get_queryset(self):
        today = timezone.now().date()
        
        if self.request.user.is_staff:
            # Определяем, что показывать админу
            show_archived = self.request.GET.get('show') == 'archived'
            
            if show_archived:
                queryset = Booking.objects.filter(tour__end_date__lt=today)
            else:
                queryset = Booking.objects.filter(tour__end_date__gte=today)
                
            queryset = queryset.select_related('tour', 'user').order_by('-booking_date')
            self.filterset = BookingFilter(self.request.GET, queryset=queryset)
            return self.filterset.qs
        else:
            # Обычные пользователи - возвращаем активные бронирования для пагинации
            return Booking.objects.filter(
                user=self.request.user,
                tour__end_date__gte=today  # Только активные
            ).select_related('tour').order_by('-booking_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()

        if self.request.user.is_staff:
            # Для админов
            current_bookings = self.filterset.qs
            context['filter'] = self.filterset
            
            # Активные фильтры
            filters_config = [
                {'key': 'search', 'label': 'Поиск', 'format': '"{value}"', 'remove_url': self._build_remove_url('search')},
                {'key': 'status', 'label': 'Статус', 'format': '{value}', 'remove_url': self._build_remove_url('status')},
                {'key': 'country', 'label': 'Страна', 'format': '"{value}"', 'remove_url': self._build_remove_url('country')},
                {'key': 'date_after', 'label': 'Дата от', 'format': '{value}', 'remove_url': self._build_remove_url('date_after')},
                {'key': 'date_before', 'label': 'Дата до', 'format': '{value}', 'remove_url': self._build_remove_url('date_before')},
            ]

            active_filters = []
            for config in filters_config:
                value = self.request.GET.get(config['key'])
                if value:
                    config['value'] = value
                    if config['key'] == 'status':
                        status_choices_dict = dict(Booking.STATUS_CHOICES)
                        config['display_value'] = status_choices_dict.get(value, value)
                    else:
                        config['display_value'] = config['format'].format(value=value)
                    active_filters.append(config)

            context['active_filters'] = active_filters
            context['has_filter'] = any(value for key, value in self.request.GET.items() if key != 'page')
            
            # Статистика для админов
            context['confirmed_count'] = current_bookings.filter(status='confirmed').count()
            context['pending_count'] = current_bookings.filter(status='pending').count()
            context['cancelled_count'] = current_bookings.filter(status='cancelled').count()
            context['total_count'] = current_bookings.count()
            context['archive_bookings'] = current_bookings.filter(tour__end_date__lt=today).order_by('-tour__end_date')

        else:
            # Для пользователей
            user_bookings = Booking.objects.filter(user=self.request.user)
            
            # Разделяем на активные и архивные
            active_bookings = user_bookings.filter(tour__end_date__gte=today)
            archive_bookings = user_bookings.filter(tour__end_date__lt=today)
            
            # Для пагинации используем только активные
            context['active_bookings'] = context['bookings']
            context['archive_bookings'] = archive_bookings.order_by('-tour__end_date')
            
            # Статистика по бронированиям пользователя
            context['confirmed_count'] = active_bookings.filter(status='confirmed').count()
            context['pending_count'] = active_bookings.filter(status='pending').count()
            context['cancelled_count'] = active_bookings.filter(status='cancelled').count()
            context['total_count'] = active_bookings.count()
            context['active_count'] = active_bookings.count()
            context['archive_count'] = archive_bookings.count()

        context['is_admin'] = self.request.user.is_staff

        # Вычисляем общую стоимость
        if self.request.user.is_staff:
            for booking in context['bookings']:
                booking.total_price = booking.tour.price * booking.persons
        else:
            for booking in context['active_bookings']:
                booking.total_price = booking.tour.price * booking.persons
            for booking in context['archive_bookings']:
                booking.total_price = booking.tour.price * booking.persons

        return context

    def _build_remove_url(self, exclude_param):
        """Создает URL без указанного параметра"""
        params = []
        for key, value in self.request.GET.items():
            if key != exclude_param and key != 'page':
                params.append(f"{key}={value}")
        return "?" + "&".join(params) if params else "?"

@login_required
@staff_required
def add_tour(request):
    """Добавление нового тура (только для админов)"""
    if request.method == 'POST':
        form = TourForm(request.POST)
        if form.is_valid():
            tour = form.save()
            messages.success(request, f'Тур "{tour.title}" успешно добавлен!')
            return redirect('tour_detail', pk=tour.id)
    else:
        form = TourForm()
    
    return render(request, 'tour_app/add_tour.html', {'form': form})

@login_required
def edit_booking(request, booking_id):
    """Редактирование бронирования"""
    if request.user.is_staff:
        booking = get_object_or_404(Booking, id=booking_id)
    else:
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            updated_booking = form.save(commit=False)
            
            # Проверяем доступность мест при изменении количества человек
            if updated_booking.persons != booking.persons:
                persons_diff = updated_booking.persons - booking.persons
                if not booking.tour.can_book(persons_diff):
                    messages.error(request,
                        f'Недостаточно свободных мест. Доступно: {booking.tour.get_available_spots()}')
                    return render(request, 'tour_app/edit_booking.html', {
                        'form': form, 
                        'booking': booking,
                        'is_admin': request.user.is_staff
                    })
            
            updated_booking.save()
            messages.success(request, 'Бронирование успешно обновлено!')
            return redirect('my_bookings')
    else:
        form = BookingForm(instance=booking)
    
    return render(request, 'tour_app/edit_booking.html', {
        'form': form, 
        'booking': booking,
        'is_admin': request.user.is_staff
    })

@login_required
def delete_booking(request, booking_id):
    """Удаление бронирования"""
    if request.user.is_staff:
        booking = get_object_or_404(Booking, id=booking_id)
    else:
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Бронирование успешно удалено!')
        return redirect('my_bookings')
    
    return render(request, 'tour_app/delete_booking.html', {
        'booking': booking,
        'is_admin': request.user.is_staff
    })

@login_required
def confirm_booking(request, booking_id):
    """Подтверждение бронирования"""
    if not request.user.is_staff:
        messages.error(request, 'Недостаточно прав для выполнения этого действия.')
        return redirect('my_bookings')
    
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Проверяем, что после подтверждения не будет превышения мест
    if not booking.tour.can_book(0):
        messages.error(request, 
            f'Нельзя подтвердить бронирование - недостаточно мест. Доступно: {booking.tour.get_available_spots()}')
        return redirect('my_bookings')
    
    booking.status = 'confirmed'
    booking.save()
    messages.success(request, f'Бронирование #{booking_id} подтверждено!')
    return redirect('my_bookings')

@login_required
def cancel_booking_admin(request, booking_id):
    """Отмена бронирования админом"""
    if not request.user.is_staff:
        messages.error(request, 'Недостаточно прав для выполнения этого действия.')
        return redirect('my_bookings')
    
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'cancelled'
    booking.save()
    messages.success(request, f'Бронирование #{booking_id} отменено администратором!')
    return redirect('my_bookings')

@login_required
@staff_required
def management_dashboard(request):
    """Единая панель управления для админов"""
    # По умолчанию - последние 30 дней
    period = request.GET.get('period', '30days')
    
    if period == '30days':
        date_filter = timezone.now() - timezone.timedelta(days=30)
    elif period == '90days':
        date_filter = timezone.now() - timezone.timedelta(days=90)
    elif period == '1year':
        date_filter = timezone.now() - timezone.timedelta(days=365)
    else:
        date_filter = None
    
    if date_filter:
        bookings = Booking.objects.filter(booking_date__gte=date_filter)
        tours = Tour.objects.filter(start_date__gte=date_filter)
        reviews = Review.objects.filter(review_date__gte=date_filter)
    else:
        tours = Tour.objects.all()
        bookings = Booking.objects.all()
        reviews = Review.objects.all()
        
    # Основные метрики
    total_tours = tours.count()
    total_bookings = bookings.count()
    total_reviews = reviews.count()
    
    # Статистика по статусам
    booking_stats = bookings.aggregate(
        pending=Count('id', filter=Q(status='pending')),
        confirmed=Count('id', filter=Q(status='confirmed')),
        cancelled=Count('id', filter=Q(status='cancelled'))
    )
    
    # Дополнительные метрики для панели
    active_tours = tours.filter(end_date__gte=timezone.now().date()).count()
    upcoming_tours = tours.filter(start_date__gte=timezone.now().date()).count()
    
    # Бронирования, требующие внимания
    pending_bookings = bookings.filter(status='pending').select_related('user', 'tour').order_by('-booking_date')[:5]
    
    # Туры с малым количеством мест
    low_availability_tours = Tour.objects.annotate(
        booked_spots=Coalesce(
            Sum('booking__persons', filter=Q(booking__status__in=['pending', 'confirmed'])), 
            0
        )
    ).annotate(
        available_spots_actual=F('available_spots') - F('booked_spots')
    ).filter(available_spots_actual__lte=3)[:5]
    
    # Популярные направления
    popular_countries = bookings.filter(status='confirmed').values(
        'tour__country'
    ).annotate(
        bookings_count=Count('id'),
        unique_customers=Count('user', distinct=True)
    ).order_by('-bookings_count')[:10]
    
    # Последние отзывы
    recent_reviews = Review.objects.select_related('user', 'tour').order_by('-review_date')[:5]
    
    # Последние бронирования
    recent_bookings = bookings.select_related('user', 'tour').order_by('-booking_date')[:5]

    context = {
        'total_tours': total_tours,
        'total_bookings': total_bookings,
        'total_reviews': total_reviews,
        'active_tours': active_tours,
        'upcoming_tours': upcoming_tours,
        'booking_stats': booking_stats,
        'pending_bookings': pending_bookings,
        'low_availability_tours': low_availability_tours,
        'popular_countries': popular_countries,
        'recent_reviews': recent_reviews,
        'recent_bookings': recent_bookings,
        'current_period': period,
    }

    return render(request, 'tour_app/management_dashboard.html', context)

@login_required
def statistics(request):
    """Общая статистика - для всех пользователей"""
    # Берем данные за последний год
    one_year_ago = timezone.now() - timezone.timedelta(days=365)
    
    # Статистика по странам за последний год
    tours_by_country = Booking.objects.filter(
        status='confirmed',
        booking_date__gte=one_year_ago
    ).values(
        'tour__country'
    ).annotate(
        total_sold=Count('id')
    ).order_by('-total_sold')
    
    # Популярные туры за последний год
    popular_tours = Tour.objects.filter(
        booking__status='confirmed',
        booking__booking_date__gte=one_year_ago
    ).annotate(
        booking_count=Count('booking')
    ).filter(booking_count__gt=0).order_by('-booking_count')[:5]
    
    # Лучшие по рейтингу туры
    top_rated_tours = Tour.objects.annotate(
        avg_rating=Avg('review__rating'),
        review_count=Count('review')
    ).filter(review_count__gte=1).order_by('-avg_rating')[:5]
    
    # Новые туры (будущие)
    upcoming_tours = Tour.objects.filter(
        start_date__gte=timezone.now().date()
    ).order_by('start_date')[:5]

    context = {
        'tours_by_country': tours_by_country,
        'popular_tours': popular_tours,
        'top_rated_tours': top_rated_tours,
        'upcoming_tours': upcoming_tours,
    }
    return render(request, 'tour_app/statistics.html', context)

@login_required
@staff_required
def delete_review(request, review_id):
    """Удаление отзыва администратором"""
    review = get_object_or_404(Review, id=review_id)
    tour_id = review.tour.id
    review.delete()
    messages.success(request, 'Отзыв успешно удален!')
    return redirect('tour_detail', pk=tour_id)