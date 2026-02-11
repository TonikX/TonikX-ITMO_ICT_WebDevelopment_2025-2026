from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.db.models import Avg, Count  # Добавь этот импорт
from django.utils import timezone
from .models import Race, Racer, Comment
from .forms import CustomUserCreationForm, RacerRegistrationForm, CommentForm, CustomUserUpdateForm


# ===== ГЛАВНАЯ СТРАНИЦА =====
def home(request):
    """
    Домашняя страница с общей статистикой.
    Показывает сколько всего гонок, участников и комментариев.
    """
    # Берем основные статистические данные
    total_races = Race.objects.count()
    total_racers = Racer.objects.count()
    total_comments = Comment.objects.count()

    # Ближайшие гонки (3 штуки)
    today = timezone.now().date()
    upcoming_races = Race.objects.filter(date__gte=today).order_by('date')[:3]

    context = {
        'total_races': total_races,
        'total_racers': total_racers,
        'total_comments': total_comments,
        'upcoming_races': upcoming_races,
    }
    return render(request, 'raceapp/home.html', context)


# ===== СПИСОК ВСЕХ ГОНОК =====
class RaceListView(ListView):
    model = Race
    template_name = 'raceapp/race_list.html'
    context_object_name = 'races'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()

        # Поиск
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(location__icontains=search_query)
            )

        # Фильтр по дате
        date_filter = self.request.GET.get('date_filter')
        if date_filter == 'upcoming':
            queryset = queryset.filter(date__gte=timezone.now().date())
        elif date_filter == 'past':
            queryset = queryset.filter(date__lt=timezone.now().date())

        # Фильтр по комментариям
        comments_filter = self.request.GET.get('comments_filter')
        if comments_filter == 'has_comments':
            queryset = queryset.annotate(comment_count=Count('comments')).filter(comment_count__gt=0)
        elif comments_filter == 'no_comments':
            queryset = queryset.annotate(comment_count=Count('comments')).filter(comment_count=0)

        # Сортировка
        sort_by = self.request.GET.get('sort', '-date')
        if sort_by in ['date', '-date', 'name', '-name']:
            queryset = queryset.order_by(sort_by)

        # Добавляем аннотации для среднего рейтинга и количества комментариев
        queryset = queryset.annotate(
            avg_rating=Avg('comments__rating'),
            comment_count=Count('comments')
        )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Статистика
        context['total_races'] = Race.objects.count()
        context['total_racers'] = Racer.objects.count()
        context['total_comments'] = Comment.objects.count()

        # Сегодняшняя дата для отображения "скоро"
        context['today'] = timezone.now().date()

        # Параметры для пагинации
        params = self.request.GET.copy()
        if 'page' in params:
            del params['page']
        context['query_params'] = params.urlencode()

        return context

# ===== ДЕТАЛЬНАЯ СТРАНИЦА ГОНКИ =====
class RaceDetailView(DetailView):
    """
    Подробная информация о конкретной гонке.
    Показывает описание, дату, место и комментарии.
    """
    model = Race
    template_name = 'raceapp/race_detail.html'
    context_object_name = 'race'

    def get_context_data(self, **kwargs):
        """Добавляем пагинированные комментарии"""
        context = super().get_context_data(**kwargs)

        # Пагинация комментариев - по 5 на страницу
        comments = self.object.comments.all().order_by('-created_at')
        paginator = Paginator(comments, 5)

        page = self.request.GET.get('page')
        try:
            comments_page = paginator.page(page)
        except PageNotAnInteger:
            comments_page = paginator.page(1)
        except EmptyPage:
            comments_page = paginator.page(paginator.num_pages)

        context['page_obj'] = comments_page
        return context


# ===== РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ =====
def register(request):
    """
    Регистрация нового пользователя в системе.
    Использует кастомную форму с доп полями.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматически логиним
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('raceapp:home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'raceapp/register.html', {'form': form})


# ===== КАСТОМНЫЙ ВХОД =====
class CustomLoginView(LoginView):
    """Просто указываем свой шаблон для входа"""
    template_name = 'raceapp/login.html'


# ===== ПОИСК ГОНОК =====
def search_races(request):
    """
    Старая функция поиска. По сути дублирует RaceListView.
    Оставляем для обратной совместимости.
    """
    query = request.GET.get('q', '')
    races = Race.objects.all()

    if query:
        races = races.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )

    # Пагинация для результатов поиска
    paginator = Paginator(races, 5)
    page = request.GET.get('page')

    try:
        races = paginator.page(page)
    except PageNotAnInteger:
        races = paginator.page(1)
    except EmptyPage:
        races = paginator.page(paginator.num_pages)

    return render(request, 'raceapp/search_results.html', {
        'races': races,
        'query': query,
    })


# ===== РЕГИСТРАЦИЯ НА ГОНКУ =====
@login_required
def racer_register(request):
    """
    Регистрация авторизованного пользователя на гонку.
    Проверяет, не зарегистрирован ли уже пользователь.
    """
    if request.method == 'POST':
        form = RacerRegistrationForm(request.POST)
        if form.is_valid():
            racer = form.save(commit=False)
            racer.user = request.user  # Привязываем текущего пользователя

            # Проверка на дублирование регистрации
            if Racer.objects.filter(user=request.user, race=racer.race).exists():
                messages.error(request, 'Вы уже зарегистрированы на эту гонку!')
                return redirect('raceapp:racer_register')

            racer.save()
            messages.success(request, 'Вы успешно зарегистрированы на гонку!')
            return redirect('raceapp:my_registrations')
    else:
        form = RacerRegistrationForm()

    return render(request, 'raceapp/racer_register.html', {'form': form})


# ===== МОИ РЕГИСТРАЦИИ =====
@login_required
def my_registrations(request):
    """
    Страница с гонками, на которые зарегистрирован пользователь.
    Админ видит ВСЕ регистрации.
    """
    if request.user.is_staff:
        # Админ видит все регистрации
        registrations = Racer.objects.all().select_related('user', 'race').order_by('-registered_at')
    else:
        # Обычный пользователь видит только свои
        registrations = Racer.objects.filter(user=request.user).select_related('race').order_by('-registered_at')

    return render(request, 'raceapp/my_registrations.html', {'registrations': registrations})

# ===== УДАЛЕНИЕ РЕГИСТРАЦИИ =====
class RacerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Удаление регистрации на гонку.
    Пользователь может удалить только свои регистрации.
    """
    model = Racer
    template_name = 'raceapp/registration_delete.html'
    success_url = reverse_lazy('raceapp:my_registrations')

    def get_queryset(self):
        """Ограничиваем доступ только к своим регистрациям"""
        return Racer.objects.filter(user=self.request.user)

    def test_func(self):
        """Проверка прав доступа"""
        racer = self.get_object()
        return racer.user == self.request.user


# ===== ДОБАВЛЕНИЕ КОММЕНТАРИЯ =====
@login_required
def add_comment(request, race_id):
    """
    Добавление комментария к конкретной гонке.
    Требует авторизации.
    """
    race = get_object_or_404(Race, pk=race_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.race = race
            comment.user = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен!')
            return redirect('raceapp:race_detail', pk=race_id)
    else:
        form = CommentForm()

    return render(request, 'raceapp/add_comment.html', {'form': form, 'race': race})


# ===== СПИСОК КОММЕНТАРИЕВ =====
class CommentListView(ListView):
    model = Comment
    template_name = 'raceapp/comment_list.html'
    context_object_name = 'comments'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()

        # Поиск
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(text__icontains=search_query) |
                Q(user__username__icontains=search_query) |
                Q(race__name__icontains=search_query)
            )

        # Фильтр по типу
        comment_type = self.request.GET.get('comment_type')
        if comment_type in ['coop', 'race', 'other']:
            queryset = queryset.filter(comment_type=comment_type)

        # Фильтр по рейтингу
        rating_filter = self.request.GET.get('rating_filter')
        if rating_filter and rating_filter.isdigit():
            queryset = queryset.filter(rating__gte=int(rating_filter))

        # Сортировка
        sort_by = self.request.GET.get('sort', '-created_at')
        if sort_by in ['created_at', '-created_at', 'rating', '-rating']:
            queryset = queryset.order_by(sort_by)

        # Оптимизация запросов
        queryset = queryset.select_related('user', 'race')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Параметры для пагинации
        params = self.request.GET.copy()
        if 'page' in params:
            del params['page']
        context['query_params'] = params.urlencode()

        return context

# ===== УДАЛЕНИЕ КОММЕНТАРИЯ =====
@login_required
def delete_comment(request, pk):
    """
    Удаление комментария.
    Может удалить автор или администратор.
    """
    comment = get_object_or_404(Comment, pk=pk)

    # Проверяем права: автор или админ
    if comment.user == request.user or request.user.is_staff:
        comment.delete()
        messages.success(request, 'Комментарий удален.')
    else:
        messages.error(request, 'Вы не можете удалить этот комментарий.')

    return redirect('raceapp:comment_list')


# ===== ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ =====
@login_required
def profile(request):
    """Страница профиля с последними регистрациями"""
    # Получаем последние 5 регистраций пользователя
    registrations = request.user.racers.all().select_related('race').order_by('-registered_at')[:5]

    # Получаем количество всех регистраций пользователя
    total_registrations = request.user.racers.count()

    return render(request, 'raceapp/profile.html', {
        'user': request.user,
        'registrations': registrations,
        'total_registrations': total_registrations
    })

# ===== РЕДАКТИРОВАНИЕ ПРОФИЛЯ =====
@login_required
def edit_profile(request):
    """
    Редактирование профиля пользователя.
    Можно изменить основные данные, но не пароль.
    """
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('raceapp:profile')
    else:
        form = CustomUserUpdateForm(instance=request.user)

    return render(request, 'raceapp/edit_profile.html', {'form': form})


# ===== СТАРАЯ ФУНКЦИЯ СПИСКА КОММЕНТАРИЕВ =====
def comment_list(request):
    """
    Старая функция для обратной совместимости.
    По сути обертка над классом CommentListView.
    """
    view = CommentListView()
    view.request = request
    view.kwargs = {}
    return view.get(request)


@login_required
def confirm_registration(request, pk):
    """
    Подтверждение регистрации гонщика.
    Доступно только администраторам.
    """
    # Проверяем, является ли пользователь администратором
    if not request.user.is_staff:
        messages.error(request, 'У вас нет прав для выполнения этого действия.')
        return redirect('raceapp:my_registrations')

    # Получаем регистрацию
    registration = get_object_or_404(Racer, pk=pk)

    # Переключаем статус подтверждения
    registration.is_confirmed = not registration.is_confirmed
    registration.save()

    status = "подтверждена" if registration.is_confirmed else "отменена"
    messages.success(request, f'Регистрация {registration.user.username} на гонку "{registration.race.name}" {status}.')

    # Возвращаемся на страницу, с которой пришли
    return redirect(request.META.get('HTTP_REFERER', 'raceapp:race_list'))


