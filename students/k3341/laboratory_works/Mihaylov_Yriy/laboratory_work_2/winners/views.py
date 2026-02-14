
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Count
from pyexpat.errors import messages

from .forms import BaseRegistrationForm, RacerProfileForm
from .forms import CommentForm
from .models import Commentator, Heat, HeatResult
from .models import Race, Comment, RaceRegistration
from django.contrib.admin.views.decorators import staff_member_required
import random


def home(request):
    if request.user.is_authenticated:
        return redirect('profile')

    return render(request, 'winners/home.html')


def base_register(request):
    if request.method == 'POST':
        form = BaseRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('choose_role')
    else:
        form = BaseRegistrationForm()

    return render(request, 'winners/base_register.html', {'form': form})


@login_required
def choose_role(request):
    if hasattr(request.user, 'racer') or hasattr(request.user, 'commentator'):
        return redirect('profile')

    return render(request, 'winners/choose_role.html')


@login_required
def register_racer(request):
    if hasattr(request.user, 'racer'):
        return redirect('profile')
    if hasattr(request.user, 'commentator'):
        return redirect('profile')

    if request.method == 'POST':
        form = RacerProfileForm(request.POST)
        if form.is_valid():
            racer = form.save(commit=False)
            racer.user = request.user
            racer.save()
            return redirect('profile')
    else:
        form = RacerProfileForm()

    return render(request, 'winners/register_racer.html', {'form': form})


@login_required
def register_commentator(request):

    Commentator.objects.create(user=request.user)
    return redirect('profile')



@login_required
def profile(request):
    context = {}
    if hasattr(request.user, 'racer'):
        context['role'] = 'racer'
        context['profile'] = request.user.racer
    elif hasattr(request.user, 'commentator'):
        context['role'] = 'commentator'
        context['profile'] = request.user.commentator
    else:
        context['role'] = 'none'

    return render(request, 'winners/profile.html', context)


def races_list(request):
    date_filter = request.GET.get('filter', 'all')

    races = Race.objects.all().order_by('race_time')

    if date_filter == 'past':
        races = races.filter(race_time__lt=timezone.now())
    elif date_filter == 'future':
        races = races.filter(race_time__gte=timezone.now())

    races = races.annotate(comments_count=Count('comment'))

    paginator = Paginator(races, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user_registrations = []
    if hasattr(request.user, 'racer'):
        user_registrations = RaceRegistration.objects.filter(
            racer=request.user.racer
        ).values_list('race_id', flat=True)

    context = {
        'page_obj': page_obj,
        'date_filter': date_filter,
        'user_registrations': user_registrations,
        'is_racer': hasattr(request.user, 'racer'),
        'is_commentator': hasattr(request.user, 'commentator'),
    }
    return render(request, 'winners/races_list.html', context)


def race_about(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    registered_racers = RaceRegistration.objects.filter(race=race, is_confirmed=True).select_related('racer__user')

    context = {
        'race': race,
        'registered_racers': registered_racers,
    }
    return render(request, 'winners/race_about.html', context)


@login_required
def race_comments(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    comments = Comment.objects.filter(race=race).order_by('-comment_time')

    if request.method == 'POST' and hasattr(request.user, 'commentator'):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.race = race
            comment.commentator = request.user.commentator
            comment.save()
            return redirect('race_comments', race_id=race_id)
    else:
        form = CommentForm()

    context = {
        'race': race,
        'comments': comments,
        'form': form,
        'is_commentator': hasattr(request.user, 'commentator'),
    }
    return render(request, 'winners/race_comments.html', context)


@login_required
def register_for_race(request, race_id):
    if not hasattr(request.user, 'racer'):
        return redirect('profile')

    race = get_object_or_404(Race, id=race_id)
    racer = request.user.racer

    if RaceRegistration.objects.filter(race=race, racer=racer).exists():
        return redirect('races_list')

    if request.method == 'POST':
        RaceRegistration.objects.create(race=race, racer=racer)
        return redirect('races_list')

    return render(request, 'winners/race_register.html', {'race': race})


@login_required
def unregister_from_race(request, race_id):
    if not hasattr(request.user, 'racer'):
        return redirect('profile')

    race = get_object_or_404(Race, id=race_id)
    racer = request.user.racer

    registration = get_object_or_404(RaceRegistration, race=race, racer=racer)
    registration.delete()

    return redirect('races_list')


def race_results(request, race_id):
    race = get_object_or_404(Race, id=race_id)

    heats = Heat.objects.filter(race=race).prefetch_related('results__racer__user')

    paginator = Paginator(heats, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    results_data = []
    for heat in page_obj:
        heat_results = heat.results.all().select_related('racer__user')
        results_data.append({
            'heat': heat,
            'results': heat_results
        })

    context = {
        'race': race,
        'results_data': results_data,
        'page_obj': page_obj,
    }
    return render(request, 'winners/race_results.html', context)


@staff_member_required
def generate_heat_results(request, heat_id):
    heat = get_object_or_404(Heat, id=heat_id)

    if request.method == 'POST':
        registrations = RaceRegistration.objects.filter(
            race=heat.race,
            is_confirmed=True
        ).select_related('racer')

        if not registrations:
            return redirect('race_results', race_id=heat.race.id)

        HeatResult.objects.filter(heat=heat).delete()

        racers = [reg.racer for reg in registrations]
        random.shuffle(racers)

        for position, racer in enumerate(racers, 1):
            HeatResult.objects.create(
                heat=heat,
                racer=racer,
                position=position
            )

        return redirect('race_results', race_id=heat.race.id)

    context = {
        'heat': heat,
        'registered_count': RaceRegistration.objects.filter(race=heat.race, is_confirmed=True).count()
    }
    return render(request, 'winners/generate_results.html', context)