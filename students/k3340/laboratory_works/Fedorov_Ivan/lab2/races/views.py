from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Race, RaceRegistration, RaceResult


def race_list(request):
    races = Race.objects.all().order_by('-date')
    return render(request, 'races/race_list.html', {'races': races})


def race_detail(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    results = RaceResult.objects.filter(race=race).order_by('position')
    registrations = RaceRegistration.objects.filter(race=race, is_confirmed=True)

    # Пагинация комментариев
    comments_list = race.comment_set.all().order_by('-created_at')
    paginator = Paginator(comments_list, 5)  # комменты пажилые
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    user_registration = None
    if request.user.is_authenticated:
        user_registration = RaceRegistration.objects.filter(race=race, user=request.user).first()

    return render(request, 'races/race_detail.html', {
        'race': race,
        'results': results,
        'registrations': registrations,
        'user_registration': user_registration,
        'page_obj': page_obj,  # Передаем пагинированные комментарии
        'comments': page_obj.object_list,  # Для совместимости
    })


@login_required
def register_for_race(request, race_id):
    race = get_object_or_404(Race, id=race_id)

    # Проверяем, не зарегистрирован ли уже пользователь
    existing_registration = RaceRegistration.objects.filter(race=race, user=request.user).first()

    if existing_registration:
        messages.warning(request, 'Вы уже зарегистрированы на эту гонку!')
    else:
        registration = RaceRegistration(race=race, user=request.user)
        registration.save()
        messages.success(request, 'Вы успешно зарегистрированы на гонку!')

    return redirect('race_detail', race_id=race_id)


@login_required
def unregister_from_race(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    registration = RaceRegistration.objects.filter(race=race, user=request.user).first()

    if registration:
        registration.delete()
        messages.success(request, 'Регистрация на гонку отменена!')
    else:
        messages.warning(request, 'Вы не были зарегистрированы на эту гонку!')

    return redirect('race_detail', race_id=race_id)