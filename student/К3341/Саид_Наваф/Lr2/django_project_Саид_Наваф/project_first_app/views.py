from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import User, Car, Team, Race, RaceRegistration, RaceComment
from .forms import CustomUserCreationForm, CarForm, RaceRegistrationForm, RaceCommentForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
# User registration view
def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect('racer_list')
    else:
        form = CustomUserCreationForm()
    # Make sure this line uses 'racer_register.html' not 'user_form.html'
    return render(request, 'project_first_app/racer_register.html', {'form': form})

# Racer views
def racer_list(request):
    """Display all racers"""
    racers = User.objects.all()
    return render(request, 'project_first_app/racer_list.html', {'racers': racers})

def racer_detail(request, racer_id):
    """Display details of a specific racer"""
    racer = get_object_or_404(User, pk=racer_id)
    registrations = RaceRegistration.objects.filter(racer=racer)
    return render(request, 'project_first_app/racer_detail.html', {
        'racer': racer,
        'registrations': registrations
    })

# Race views
class RaceListView(ListView):
    model = Race
    template_name = 'project_first_app/race_list.html'
    context_object_name = 'races'
    ordering = ['-date']

class RaceDetailView(DetailView):
    model = Race
    template_name = 'project_first_app/race_detail.html'
    context_object_name = 'race'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registrations'] = RaceRegistration.objects.filter(race=self.object).order_by('final_position')
        context['comments'] = RaceComment.objects.filter(race=self.object).order_by('-created_date')
        return context

@login_required
def race_register(request, race_id):
    """Register for a race"""
    race = get_object_or_404(Race, pk=race_id)
    
    if request.method == 'POST':
        form = RaceRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.racer = request.user
            registration.race = race
            registration.save()
            return redirect('race_detail', pk=race_id)
    else:
        form = RaceRegistrationForm(initial={'race': race})
    
    return render(request, 'project_first_app/race_register.html', {
        'form': form,
        'race': race
    })

@login_required
def race_unregister(request, registration_id):
    """Unregister from a race"""
    registration = get_object_or_404(RaceRegistration, pk=registration_id, racer=request.user)
    race_id = registration.race.id
    registration.delete()
    return redirect('race_detail', pk=race_id)

@login_required
def add_race_comment(request, race_id):
    """Add comment to a race"""
    race = get_object_or_404(Race, pk=race_id)
    
    if request.method == 'POST':
        form = RaceCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.race = race
            comment.save()
            return redirect('race_detail', pk=race_id)
    else:
        form = RaceCommentForm(initial={'race': race})
    
    return render(request, 'project_first_app/race_comment.html', {
        'form': form,
        'race': race
    })

# Car views (keep existing but update template names)
class CarListView(ListView):
    model = Car
    template_name = 'project_first_app/car_list.html'
    context_object_name = 'cars'

class CarDetailView(DetailView):
    model = Car
    template_name = 'project_first_app/car_detail.html'
    context_object_name = 'car'

class CarCreateView(CreateView):
    model = Car
    form_class = CarForm
    template_name = 'project_first_app/car_form.html'
    success_url = reverse_lazy('car_list')

class CarUpdateView(UpdateView):
    model = Car
    form_class = CarForm
    template_name = 'project_first_app/car_form.html'
    success_url = reverse_lazy('car_list')

class CarDeleteView(DeleteView):
    model = Car
    template_name = 'project_first_app/car_confirm_delete.html'
    success_url = reverse_lazy('car_list')

# Team views
class TeamListView(ListView):
    model = Team
    template_name = 'project_first_app/team_list.html'
    context_object_name = 'teams'

class TeamDetailView(DetailView):
    model = Team
    template_name = 'project_first_app/team_detail.html'
    context_object_name = 'team'

# Results view
def race_results(request):
    """Display all race results from last month"""
    last_month = timezone.now().date() - timedelta(days=30)
    recent_races = Race.objects.filter(date__gte=last_month)
    recent_registrations = RaceRegistration.objects.filter(race__in=recent_races).exclude(final_position__isnull=True)
    
    return render(request, 'project_first_app/race_results.html', {
        'recent_races': recent_races,
        'recent_registrations': recent_registrations,
        'last_month': last_month
    })

def home(request):
    """Home page with navigation"""
    recent_races = Race.objects.filter(date__gte=timezone.now().date()).order_by('date')[:5]
    top_racers = User.objects.filter(raceregistration__final_position=1).distinct()[:5]
    
    return render(request, 'project_first_app/home.html', {
        'recent_races': recent_races,
        'top_racers': top_racers
    })