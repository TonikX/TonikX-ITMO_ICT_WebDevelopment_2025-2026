"""
Views для приложения racing.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from .models import Race, Heat, HeatResult, Registration, DriverProfile, Comment
from .forms import RegistrationForm, CommentForm, DriverProfileForm


class OwnerRequiredMixin:
    """Миксин для проверки, что пользователь является владельцем объекта или админом."""
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        
        # Админы (staff/superuser) могут редактировать всё
        if self.request.user.is_staff or self.request.user.is_superuser:
            return obj
        
        # Проверяем, что текущий пользователь - владелец объекта
        if hasattr(obj, 'driver'):
            # Для Registration
            if obj.driver.user != self.request.user:
                raise PermissionDenied("Вы не можете редактировать чужую регистрацию.")
        elif hasattr(obj, 'author'):
            # Для Comment
            if obj.author != self.request.user:
                raise PermissionDenied("Вы не можете редактировать чужой комментарий.")
        elif hasattr(obj, 'user'):
            # Для DriverProfile
            if obj.user != self.request.user:
                raise PermissionDenied("Вы не можете редактировать чужой профиль.")
        return obj


class RaceListView(ListView):
    """Список опубликованных гонок с поиском."""
    model = Race
    template_name = 'racing/race_list.html'
    context_object_name = 'races'
    paginate_by = 6
    
    def get_queryset(self):
        queryset = Race.objects.filter(is_published=True)
        
        # Поиск по названию и месту
        search_query = self.request.GET.get('search', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(location__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        # Сортировка
        sort_by = self.request.GET.get('sort', '-date')
        if sort_by in ['date', '-date', 'title', '-title', 'location', '-location']:
            queryset = queryset.order_by(sort_by)
        else:
            queryset = queryset.order_by('-date')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['current_sort'] = self.request.GET.get('sort', '-date')
        
        # Для сохранения параметров поиска в пагинации
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            query_params.pop('page')
        context['query_string'] = query_params.urlencode()
        
        return context


class RaceDetailView(DetailView):
    """Детальная информация о гонке."""
    model = Race
    template_name = 'racing/race_detail.html'
    context_object_name = 'race'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        race = self.object
        
        # Получаем заезды
        heats = race.heats.all().prefetch_related('results__driver__team')
        context['heats'] = heats
        
        # Для каждого заезда получаем результаты отсортированные по позиции
        heats_with_results = []
        for heat in heats:
            results = heat.results.select_related('driver', 'driver__team').order_by('position', 'finish_time_seconds')
            heats_with_results.append({
                'heat': heat,
                'results': results
            })
        context['heats_with_results'] = heats_with_results
        
        # Регистрации на эту гонку с поиском и пагинацией
        registrations = race.registrations.filter(active=True).select_related('driver', 'driver__team')
        
        # Поиск по участникам
        search_participants = self.request.GET.get('search_participants', '').strip()
        if search_participants:
            registrations = registrations.filter(
                Q(driver__full_name__icontains=search_participants) |
                Q(driver__team__name__icontains=search_participants) |
                Q(driver__car_description__icontains=search_participants) |
                Q(car_number__icontains=search_participants)
            )
        
        # Сортировка участников
        sort_participants = self.request.GET.get('sort_participants', 'car_number')
        if sort_participants in ['car_number', '-car_number', 'driver__full_name', '-driver__full_name', 
                                  'driver__team__name', '-driver__team__name', 'driver__driver_class', '-driver__driver_class']:
            registrations = registrations.order_by(sort_participants)
        else:
            registrations = registrations.order_by('car_number')
        
        # Пагинация участников
        from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
        paginator = Paginator(registrations, 6)  # 6 участников на страницу
        page = self.request.GET.get('page_participants')
        
        try:
            registrations_page = paginator.page(page)
        except PageNotAnInteger:
            registrations_page = paginator.page(1)
        except EmptyPage:
            registrations_page = paginator.page(paginator.num_pages)
        
        context['registrations'] = registrations_page
        context['registrations_total'] = paginator.count
        context['search_participants'] = search_participants
        context['sort_participants'] = sort_participants
        
        # Параметры для пагинации участников
        query_params_participants = self.request.GET.copy()
        if 'page_participants' in query_params_participants:
            query_params_participants.pop('page_participants')
        context['query_string_participants'] = query_params_participants.urlencode()
        
        # Комментарии
        context['comments'] = race.comments.all().select_related('author').order_by('-created_at')
        
        # Проверка прав админа
        context['is_admin'] = self.request.user.is_authenticated and (
            self.request.user.is_staff or self.request.user.is_superuser
        )
        
        # Проверяем, зарегистрирован ли текущий пользователь
        if self.request.user.is_authenticated:
            try:
                context['user_registration'] = Registration.objects.get(
                    driver=self.request.user.driver_profile,
                    race=race,
                    active=True
                )
            except (Registration.DoesNotExist, DriverProfile.DoesNotExist):
                context['user_registration'] = None
            
            # Формы
            context['registration_form'] = RegistrationForm()
            context['comment_form'] = CommentForm()
        
        return context


@login_required
def register_for_race(request, pk):
    """Регистрация на гонку."""
    race = get_object_or_404(Race, pk=pk)
    
    try:
        driver_profile = request.user.driver_profile
        # Проверяем, что профиль заполнен
        if not driver_profile.full_name or driver_profile.full_name.strip() == '':
            messages.warning(request, 'Для регистрации на гонку сначала заполните свой профиль водителя.')
            return redirect('driverprofile_update')
    except DriverProfile.DoesNotExist:
        messages.error(request, 'Сначала заполните профиль водителя.')
        return redirect('driverprofile_update')
    
    # Проверяем, не зарегистрирован ли уже
    existing = Registration.objects.filter(driver=driver_profile, race=race, active=True).first()
    if existing:
        messages.warning(request, 'Вы уже зарегистрированы на эту гонку.')
        return redirect('race_detail', pk=race.pk)
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.driver = driver_profile
            registration.race = race
            registration.save()
            messages.success(request, 'Вы успешно зарегистрированы на гонку!')
            return redirect('race_detail', pk=race.pk)
    
    return redirect('race_detail', pk=race.pk)


@login_required
def unregister_from_race(request, pk):
    """Отмена регистрации на гонку."""
    race = get_object_or_404(Race, pk=pk)
    
    try:
        driver_profile = request.user.driver_profile
        registration = Registration.objects.get(driver=driver_profile, race=race, active=True)
        registration.active = False
        registration.save()
        messages.success(request, 'Регистрация отменена.')
    except (DriverProfile.DoesNotExist, Registration.DoesNotExist):
        messages.error(request, 'Регистрация не найдена.')
    
    return redirect('race_detail', pk=race.pk)


@login_required
def add_comment(request, pk):
    """Добавление комментария к гонке."""
    race = get_object_or_404(Race, pk=pk)
    
    # Проверяем, что профиль заполнен
    try:
        if not request.user.driver_profile.full_name or request.user.driver_profile.full_name.strip() == '':
            messages.warning(request, 'Для добавления комментария сначала заполните свой профиль.')
            return redirect('driverprofile_update')
    except DriverProfile.DoesNotExist:
        messages.warning(request, 'Для добавления комментария сначала заполните свой профиль.')
        return redirect('driverprofile_update')
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.race = race
            comment.author = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен!')
            return redirect('race_detail', pk=race.pk)
        else:
            messages.error(request, 'Ошибка в форме комментария.')
    
    return redirect('race_detail', pk=race.pk)


class RegistrationListView(LoginRequiredMixin, ListView):
    """Список регистраций текущего пользователя (или всех для админа) с поиском."""
    model = Registration
    template_name = 'racing/registration_list.html'
    context_object_name = 'registrations'
    paginate_by = 15
    
    def get_queryset(self):
        is_admin = self.request.user.is_staff or self.request.user.is_superuser
        
        # Базовый queryset
        if is_admin:
            queryset = Registration.objects.filter(
                active=True
            ).select_related('race', 'driver', 'driver__team', 'driver__user')
        else:
            try:
                driver_profile = self.request.user.driver_profile
                queryset = Registration.objects.filter(
                    driver=driver_profile,
                    active=True
                ).select_related('race', 'driver__team')
            except DriverProfile.DoesNotExist:
                return Registration.objects.none()
        
        # Поиск
        search_query = self.request.GET.get('search', '').strip()
        if search_query:
            if is_admin:
                # Админы могут искать по водителю и гонке
                queryset = queryset.filter(
                    Q(race__title__icontains=search_query) |
                    Q(race__location__icontains=search_query) |
                    Q(driver__full_name__icontains=search_query) |
                    Q(driver__user__username__icontains=search_query)
                )
            else:
                # Обычные пользователи ищут только по гонкам
                queryset = queryset.filter(
                    Q(race__title__icontains=search_query) |
                    Q(race__location__icontains=search_query)
                )
        
        # Сортировка
        sort_by = self.request.GET.get('sort', '-created_at')
        valid_sorts = ['-created_at', 'created_at', 'race__date', '-race__date', 'race__title', '-race__title']
        if sort_by in valid_sorts:
            queryset = queryset.order_by(sort_by)
        else:
            queryset = queryset.order_by('-created_at')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = self.request.user.is_staff or self.request.user.is_superuser
        context['search_query'] = self.request.GET.get('search', '')
        context['current_sort'] = self.request.GET.get('sort', '-created_at')
        
        # Для сохранения параметров поиска в пагинации
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            query_params.pop('page')
        context['query_string'] = query_params.urlencode()
        
        return context


class RegistrationUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    """Редактирование регистрации."""
    model = Registration
    form_class = RegistrationForm
    template_name = 'racing/registration_form.html'
    success_url = reverse_lazy('registration_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Регистрация обновлена.')
        return super().form_valid(form)


class RegistrationDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    """Удаление регистрации."""
    model = Registration
    template_name = 'racing/registration_confirm_delete.html'
    success_url = reverse_lazy('registration_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Регистрация удалена.')
        return super().delete(request, *args, **kwargs)


class DriverProfileDetailView(LoginRequiredMixin, DetailView):
    """Просмотр профиля водителя."""
    model = DriverProfile
    template_name = 'racing/driverprofile_detail.html'
    context_object_name = 'profile'
    
    def get_object(self):
        return self.request.user.driver_profile
    
    def get(self, request, *args, **kwargs):
        """Если профиль не заполнен, редирект на редактирование."""
        profile = self.get_object()
        if not profile.full_name or profile.full_name.strip() == '':
            messages.info(request, 'Пожалуйста, заполните свой профиль водителя.')
            return redirect('driverprofile_update')
        return super().get(request, *args, **kwargs)


class DriverProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля водителя."""
    model = DriverProfile
    form_class = DriverProfileForm
    template_name = 'racing/driverprofile_form.html'
    success_url = reverse_lazy('driverprofile_detail')
    
    def get_object(self):
        return self.request.user.driver_profile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Проверяем, первое ли это заполнение профиля
        profile = self.get_object()
        context['is_first_time'] = not profile.full_name or profile.full_name.strip() == ''
        return context
    
    def form_valid(self, form):
        is_first_time = not self.get_object().full_name or self.get_object().full_name.strip() == ''
        response = super().form_valid(form)
        
        if is_first_time:
            messages.success(self.request, 'Добро пожаловать! Ваш профиль водителя успешно создан.')
        else:
            messages.success(self.request, 'Профиль обновлен.')
        
        return response


class CommentUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    """Редактирование комментария."""
    model = Comment
    form_class = CommentForm
    template_name = 'racing/comment_form.html'
    
    def get_success_url(self):
        return reverse('race_detail', kwargs={'pk': self.object.race.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Комментарий обновлен.')
        return super().form_valid(form)


class CommentDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    """Удаление комментария."""
    model = Comment
    template_name = 'racing/comment_confirm_delete.html'
    
    def get_success_url(self):
        return reverse('race_detail', kwargs={'pk': self.object.race.pk})
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Комментарий удален.')
        return super().delete(request, *args, **kwargs)


def signup(request):
    """Регистрация нового пользователя."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна! Теперь заполните свой профиль водителя.')
            return redirect('driverprofile_update')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})

