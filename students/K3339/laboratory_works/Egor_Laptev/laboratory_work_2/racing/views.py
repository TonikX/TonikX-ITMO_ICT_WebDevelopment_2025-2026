from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Race, Registration, ParticipantProfile, Comment, Car
from .forms import RegistrationForm, CommentForm, ParticipantProfileForm, CarForm
from django.contrib import messages
from django.views.generic import ListView


class RaceListView(ListView):
    model = Race
    template_name = "racing/race_list.html"
    context_object_name = "races"
    ordering = ["-date"]
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get("q")

        if q:
            queryset = queryset.filter(title__icontains=q)

        return queryset


def race_list(request):
    races = Race.objects.order_by('-date')
    return render(request, 'racing/race_list.html', {'races': races})


def race_detail(request, pk):
    race = get_object_or_404(Race, pk=pk)
    registrations = race.registrations.select_related('participant', 'car').order_by(
        'position')  # позиция может быть null
    comments = race.comments.select_related('commentator').order_by('-created_at')
    
    # Получаем регистрацию текущего пользователя, если он зарегистрирован
    user_registration = None
    has_profile = False
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            has_profile = True
            user_registration = Registration.objects.filter(race=race, participant=profile).first()
        except ParticipantProfile.DoesNotExist:
            pass
    
    return render(request, 'racing/race_detail.html', {
        'race': race,
        'registrations': registrations,
        'comments': comments,
        'comment_form': CommentForm(),
        'user_registration': user_registration,
        'has_profile': has_profile,
    })


@login_required
def register_for_race(request, race_pk):
    race = get_object_or_404(Race, pk=race_pk)
    profile, _ = ParticipantProfile.objects.get_or_create(user=request.user, defaults={
        'full_name': request.user.get_full_name() or request.user.username})
    
    # Проверка наличия автомобилей
    cars_count = profile.cars.count()
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST, user=request.user)
        if form.is_valid():
            reg = form.save(commit=False)
            reg.race = race
            reg.participant = profile
            # проверка уникальности — unique_together обеспечит, но лучше показать сообщение
            if Registration.objects.filter(race=race, participant=profile).exists():
                messages.error(request, "Вы уже зарегистрированы на эту гонку.")
                return redirect('racing:race_detail', pk=race.pk)
            reg.save()
            messages.success(request, "Регистрация успешно выполнена.")
            return redirect('racing:race_detail', pk=race.pk)
    else:
        form = RegistrationForm(user=request.user)
    return render(request, 'racing/register.html', {
        'form': form, 
        'race': race,
        'cars_count': cars_count
    })


@login_required
def edit_registration(request, reg_pk):
    reg = get_object_or_404(Registration, pk=reg_pk, participant__user=request.user)
    if request.method == 'POST':
        form = RegistrationForm(request.POST, instance=reg, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Регистрация обновлена.")
            return redirect('racing:race_detail', pk=reg.race.pk)
    else:
        form = RegistrationForm(instance=reg, user=request.user)
    return render(request, 'racing/edit_registration.html', {'form': form, 'registration': reg, 'race': reg.race})


@login_required
def cancel_registration(request, reg_pk):
    reg = get_object_or_404(Registration, pk=reg_pk, participant__user=request.user)
    if request.method == 'POST':
        reg.delete()
        messages.success(request, "Регистрация удалена.")
        return redirect('racing:race_detail', pk=reg.race.pk)
    return render(request, 'racing/confirm_delete.html', {'object': reg})


@login_required
def add_comment(request, race_pk):
    race = get_object_or_404(Race, pk=race_pk)
    # Проверка наличия профиля участника для комментатора
    if not hasattr(request.user, 'profile'):
        messages.error(request, "Для добавления комментария необходимо создать профиль участника.")
        return redirect('racing:edit_profile')
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.race = race
            comment.commentator = request.user
            comment.save()
            messages.success(request, "Комментарий добавлен.")
    return redirect('racing:race_detail', pk=race.pk)


@login_required
def edit_profile(request):
    profile, _ = ParticipantProfile.objects.get_or_create(user=request.user, defaults={
        'full_name': request.user.get_full_name() or request.user.username})
    if request.method == 'POST':
        form = ParticipantProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль обновлён.")
            return redirect('racing:profile')
    else:
        form = ParticipantProfileForm(instance=profile)
    return render(request, 'racing/edit_profile.html', {'form': form})


@login_required
def profile_view(request):
    profile, _ = ParticipantProfile.objects.get_or_create(user=request.user, defaults={
        'full_name': request.user.get_full_name() or request.user.username})
    cars = profile.cars.all()
    regs = profile.registrations.select_related('race').all()
    return render(request, 'racing/profile.html', {'profile': profile, 'cars': cars, 'registrations': regs})


@login_required
def add_car(request):
    profile = ParticipantProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = profile
            car.save()
            messages.success(request, "Автомобиль добавлен.")
            return redirect('racing:profile')
    else:
        form = CarForm()
    return render(request, 'racing/add_car.html', {'form': form})


def leaderboard(request):
    """Табло победителей - показывает все гонки с их результатами"""
    races = Race.objects.prefetch_related(
        'registrations__participant',
        'registrations__car'
    ).all().order_by('-date')
    
    # Для каждой гонки получаем топ-3 результата
    races_with_results = []
    for race in races:
        top_results = race.registrations.filter(
            position__isnull=False
        ).select_related('participant', 'car').order_by('position')[:3]
        
        races_with_results.append({
            'race': race,
            'top_results': top_results,
            'total_participants': race.registrations.count(),
            'has_results': top_results.exists()
        })
    
    return render(request, 'racing/leaderboard.html', {
        'races_with_results': races_with_results
    })


def register_user(request):
    """Регистрация нового пользователя"""
    if request.user.is_authenticated:
        return redirect('racing:race_list')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Автоматически создаем профиль участника
            ParticipantProfile.objects.create(
                user=user,
                full_name=user.username
            )
            # Автоматически входим пользователя после регистрации
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}! Ваш аккаунт успешно создан.')
            return redirect('racing:race_list')
    else:
        form = UserCreationForm()
    
    return render(request, 'racing/register_user.html', {'form': form})


@login_required
def logout_user(request):
    """Выход из системы"""
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('racing:race_list')
