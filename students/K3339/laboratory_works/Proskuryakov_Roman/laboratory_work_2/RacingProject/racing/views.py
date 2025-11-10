from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator
from django.urls import reverse
from django.views.decorators.http import require_POST
from .models import Profile, Participant, Car, Race, Registration, RaceSession, RaceResult, Comment, Team
from .forms import ProfileRegistrationForm, ParticipantForm, CarForm, RaceRegistrationForm, CommentForm, RaceForm, RaceSessionForm, RaceResultForm, TeamForm

def next_redirect(request, urlname):
    next_url = request.GET.get("next")
    if next_url:
        return redirect(next_url)
    
    return redirect(urlname)

def index(request):
    # simple index showing login (or welcome if authenticated)
    # if request.user.is_authenticated:
    #     return redirect('racing:races_list')
    return render(request, 'racing/index.html')

class AppLoginView(LoginView):
    template_name = 'racing/login.html'

def register(request):
    if request.method == 'POST':
        form = ProfileRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # create Profile automatically in signal or here
            profile, _ = Profile.objects.get_or_create(user=user)
            login(request, user)
            return redirect('racing:races_list')
    else:
        form = ProfileRegistrationForm()
    return render(request, 'racing/register.html', {'form': form})

@login_required
def participant_create(request):
    try:
        request.user.profile.participant
        return next_redirect(request, 'racing:races_list')
    except Exception:
        pass

    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.profile = request.user.profile
            participant.save()

            return next_redirect(request, 'racing:races_list')
    else:
        form = ParticipantForm()
    return render(request, 'racing/participant_form.html', {'form': form})

@login_required
def participant_edit(request):
    profile = request.user.profile
    participant = getattr(profile, 'participant', None)
    if not participant:
        return redirect('racing:races_list')
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            return redirect('racing:races_list')
    else:
        form = ParticipantForm(instance=participant)
    return render(request, 'racing/participant_edit.html', {'form': form})

@login_required
def car_create(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save()
            return redirect('racing:races_list')
    else:
        form = CarForm()
    return render(request, 'racing/car_form.html', {'form': form})

@login_required
def team_create(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save()
            return redirect('racing:races_list')
    else:
        form = TeamForm()
    return render(request, 'racing/team_form.html', {'form': form})

def races_list(request):
    qs = Race.objects.all().order_by('-date')
    paginator = Paginator(qs, 2)
    page = request.GET.get('page', 1)
    races = paginator.get_page(page)
    try:
        registered_races = request.user.profile.participant.registrations.values_list('race_id', flat=True)
    except Exception:
        registered_races = []
        
    return render(request, 'racing/races_list.html', {'races': races, 'registered_races': registered_races})

def race_detail(request, pk):
    race = get_object_or_404(Race, pk=pk)
    sessions = race.sessions.all().order_by('order').prefetch_related('results__registration__participant','results')
    participants = Participant.objects.filter(registrations__race=race).distinct()

    registrations = race.registrations.all().order_by('created_at')
    
    comment_form = CommentForm()
    return render(request, 'racing/race_detail.html', {'race': race, 'sessions': sessions, 'comment_form': comment_form})

@login_required
def race_register(request, race_pk):
    race = get_object_or_404(Race, pk=race_pk)
    cars = Car.objects.all()
    profile = request.user.profile
    try:
        participant = profile.participant
    except Exception:
        return redirect(f"{reverse('racing:participant_create')}?next=/races/{race_pk}/register/")

    exists = Registration.objects.filter(
        participant=participant,
        race=race
    ).exists()
    # уже зарегестрированно
    if exists:
        return redirect('racing:race_detail', pk=race.pk)
    
    if request.method == 'POST':
        form = RaceRegistrationForm(request.POST, profile=profile, race=race)
        if form.is_valid():
            reg = form.save(commit=False)
            reg.race = race        # <-- обязательное заполнение
            reg.save()
            return redirect('racing:race_detail', pk=race.pk)
    else:
        form = RaceRegistrationForm(profile=profile, race=race)
    return render(request, 'racing/race_register.html', {'race': race, 'form': form, 'cars': cars, 'participant': participant})

@login_required
def race_create(request):
    profile = request.user.profile
    if not profile.isAdmin():
        return redirect('racing:races_list')

    if request.method == "POST":
        form = RaceForm(request.POST)
        if form.is_valid():
            race = form.save(commit=False)
            race.created_by = request.user.profile  # ← кто создал гонку
            race.save()
            return next_redirect(request, "racing:races_list")  # после создания — в список гонок
    else:
        form = RaceForm()

    return render(request, "racing/race_create.html", {"form": form})


@login_required
def race_unregister(request, race_pk):
    race = get_object_or_404(Race, pk=race_pk)
    profile = request.user.profile
    participant = profile.participant

    Registration.objects.filter(
        participant=participant,
        race=race
    ).delete()
    # race = get_object_or_404(Race, pk=race_pk)
    # participant_id = request.POST.get('participant_id')
    # car_id = request.POST.get('car_id')
    # participant = get_object_or_404(Participant, pk=participant_id, profile=request.user.profile)
    # car = get_object_or_404(Car, pk=car_id)
    # reg, created = Registration.objects.get_or_create(participant=participant, car=car, race=race)
    # if not created:
    #     reg.delete()
    return next_redirect(request, 'racing:races_list')

@login_required
@require_POST
def add_comment(request, race_pk):
    race = get_object_or_404(Race, pk=race_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.race = race
        comment.profile = request.user.profile
        comment.save()
    return redirect('racing:race_detail', pk=race.pk)

@login_required
def race_session_create(request, race_pk):
    profile = request.user.profile
    if not profile.isAdmin():
        return redirect('racing:races_list')

    race = get_object_or_404(Race, pk=race_pk)

    if request.method == "POST":
        form = RaceSessionForm(request.POST)
        if form.is_valid():
            race_session = form.save(commit=False)
            race_session.race = race
            race_session.save()
            return next_redirect(request, "racing:races_list")  # после создания — в список гонок
    else:
        form = RaceSessionForm()

    return render(request, "racing/race_session_create.html", {"form": form})

@login_required
def add_result(request, race_pk, session_pk):
    profile = request.user.profile
    if not profile.isAdmin():
        return redirect('racing:races_list')

    race = get_object_or_404(Race, pk=race_pk)
    session = get_object_or_404(RaceSession, pk=session_pk, race=race)

    if request.method == "POST":
        form = RaceResultForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.session = session
            result.save()
            return redirect('racing:race_detail', pk=race.pk)
    else:
        form = RaceResultForm(initial={"session": session})

    return render(request, "racing/result_create.html", {"form": form, "race": race, "session": session})
