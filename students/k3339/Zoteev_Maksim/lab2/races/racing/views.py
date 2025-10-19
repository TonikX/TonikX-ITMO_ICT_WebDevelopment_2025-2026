from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count
from django.utils import timezone
from .models import Race, Participant, RaceParticipant, Comment, Team, Car
from .forms import (
    UserRegistrationForm,
    ParticipantProfileForm,
    CommentForm,
    RaceRegistrationForm,
    RaceResultForm,
)


def is_admin(user):
    """Check if user is admin/staff"""
    return user.is_staff or user.is_superuser


def index(request):
    """Home page with race list"""
    races = Race.objects.all()

    # Filtering
    status_filter = request.GET.get("status", "")
    location_filter = request.GET.get("location", "")
    search_query = request.GET.get("q", "")

    if status_filter:
        races = races.filter(status=status_filter)
    if location_filter:
        races = races.filter(location__icontains=location_filter)
    if search_query:
        races = races.filter(
            Q(name__icontains=search_query)
            | Q(location__icontains=search_query)
            | Q(description__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(races, 9)  # 9 races per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Get unique locations for filter dropdown
    locations = Race.objects.values_list("location", flat=True).distinct()

    context = {
        "page_obj": page_obj,
        "status_filter": status_filter,
        "location_filter": location_filter,
        "search_query": search_query,
        "locations": locations,
    }
    return render(request, "racing/index.html", context)


def race_detail(request, race_id):
    """Race detail page with participants and comments"""
    race = get_object_or_404(Race, id=race_id)
    race_participants = RaceParticipant.objects.filter(race=race).select_related(
        "participant", "participant__team", "participant__car"
    )
    comments = Comment.objects.filter(race=race).select_related("author")

    # Calculate average rating
    avg_rating = comments.aggregate(Avg("rating"))["rating__avg"]

    # Check if user is registered for this race
    user_registered = False
    if request.user.is_authenticated and hasattr(request.user, "participant_profile"):
        user_registered = RaceParticipant.objects.filter(
            race=race, participant=request.user.participant_profile
        ).exists()

    # Pagination for comments
    paginator = Paginator(comments, 10)
    page_number = request.GET.get("page")
    comments_page = paginator.get_page(page_number)

    context = {
        "race": race,
        "race_participants": race_participants,
        "comments_page": comments_page,
        "avg_rating": avg_rating,
        "user_registered": user_registered,
    }
    return render(request, "racing/race_detail.html", context)


def leaderboard(request):
    """Leaderboard showing top participants by total points"""
    participants = Participant.objects.all()

    # Filtering
    team_filter = request.GET.get("team", "")
    experience_filter = request.GET.get("experience", "")

    if team_filter:
        participants = participants.filter(team_id=team_filter)
    if experience_filter:
        participants = participants.filter(experience_level=experience_filter)

    # Calculate total points for each participant
    participant_stats = []
    for participant in participants:
        total_points = (
            RaceParticipant.objects.filter(participant=participant).aggregate(
                total=models.Sum("points")
            )["total"]
            or 0
        )

        total_races = RaceParticipant.objects.filter(participant=participant).count()
        wins = RaceParticipant.objects.filter(
            participant=participant, position=1
        ).count()

        participant_stats.append(
            {
                "participant": participant,
                "total_points": total_points,
                "total_races": total_races,
                "wins": wins,
            }
        )

    # Sort by total points
    participant_stats.sort(key=lambda x: x["total_points"], reverse=True)

    # Pagination
    paginator = Paginator(participant_stats, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    teams = Team.objects.all()

    context = {
        "page_obj": page_obj,
        "team_filter": team_filter,
        "experience_filter": experience_filter,
        "teams": teams,
    }
    return render(request, "racing/leaderboard.html", context)


def register_user(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                "Registration successful! Please complete your participant profile.",
            )
            return redirect("create_profile")
    else:
        form = UserRegistrationForm()

    return render(request, "racing/register.html", {"form": form})


def login_user(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("index")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "racing/login.html")


@login_required
def logout_user(request):
    """User logout view"""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("index")


@login_required
def create_profile(request):
    """Create participant profile"""
    # Check if user already has a profile
    if hasattr(request.user, "participant_profile"):
        messages.info(request, "You already have a profile.")
        return redirect("profile")

    if request.method == "POST":
        form = ParticipantProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "Profile created successfully!")
            return redirect("profile")
    else:
        # Pre-fill full name from user data
        initial_data = {
            "full_name": f"{request.user.first_name} {request.user.last_name}".strip()
        }
        form = ParticipantProfileForm(initial=initial_data)

    return render(request, "racing/create_profile.html", {"form": form})


@login_required
def profile(request):
    """View and edit user profile"""
    if not hasattr(request.user, "participant_profile"):
        messages.warning(request, "Please create your participant profile first.")
        return redirect("create_profile")

    participant = request.user.participant_profile

    if request.method == "POST":
        form = ParticipantProfileForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")
    else:
        form = ParticipantProfileForm(instance=participant)

    # Get user's race history
    race_history = RaceParticipant.objects.filter(
        participant=participant
    ).select_related("race")

    context = {
        "form": form,
        "participant": participant,
        "race_history": race_history,
    }
    return render(request, "racing/profile.html", context)


@login_required
def register_for_race(request, race_id):
    """Register participant for a race"""
    race = get_object_or_404(Race, id=race_id)

    # Check if user has a participant profile
    if not hasattr(request.user, "participant_profile"):
        messages.warning(request, "Please create your participant profile first.")
        return redirect("create_profile")

    participant = request.user.participant_profile

    # Check if race is upcoming
    if race.status != "upcoming":
        messages.error(request, "Registration is only allowed for upcoming races.")
        return redirect("race_detail", race_id=race_id)

    # Check if already registered
    if RaceParticipant.objects.filter(race=race, participant=participant).exists():
        messages.warning(request, "You are already registered for this race.")
        return redirect("race_detail", race_id=race_id)

    # Register participant
    RaceParticipant.objects.create(race=race, participant=participant)
    messages.success(request, f"Successfully registered for {race.name}!")
    return redirect("race_detail", race_id=race_id)


@login_required
def add_comment(request, race_id):
    """Add comment/review to a race"""
    race = get_object_or_404(Race, id=race_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.race = race
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment added successfully!")
            return redirect("race_detail", race_id=race_id)

    return redirect("race_detail", race_id=race_id)


@login_required
@user_passes_test(is_admin)
def manage_race_results(request, race_id):
    """Admin view to manage race results"""
    race = get_object_or_404(Race, id=race_id)
    race_participants = RaceParticipant.objects.filter(race=race).select_related(
        "participant"
    )

    if request.method == "POST":
        # Update race status
        race.status = request.POST.get("race_status", race.status)
        race.save()

        # Update participant results
        for rp in race_participants:
            form = RaceResultForm(request.POST, instance=rp, prefix=f"rp_{rp.id}")
            if form.is_valid():
                form.save()

        messages.success(request, "Race results updated successfully!")
        return redirect("manage_race_results", race_id=race_id)

    # Create forms for each participant
    participant_forms = []
    for rp in race_participants:
        form = RaceResultForm(instance=rp, prefix=f"rp_{rp.id}")
        participant_forms.append((rp, form))

    context = {
        "race": race,
        "participant_forms": participant_forms,
    }
    return render(request, "racing/manage_results.html", context)


def teams_list(request):
    """List of all teams"""
    teams = Team.objects.all()

    # Search
    search_query = request.GET.get("q", "")
    if search_query:
        teams = teams.filter(
            Q(name__icontains=search_query) | Q(country__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(teams, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "search_query": search_query,
    }
    return render(request, "racing/teams_list.html", context)


def cars_list(request):
    """List of all cars"""
    cars = Car.objects.all()

    # Search and filter
    search_query = request.GET.get("q", "")
    manufacturer_filter = request.GET.get("manufacturer", "")

    if search_query:
        cars = cars.filter(
            Q(model_name__icontains=search_query)
            | Q(manufacturer__icontains=search_query)
        )
    if manufacturer_filter:
        cars = cars.filter(manufacturer=manufacturer_filter)

    manufacturers = Car.objects.values_list("manufacturer", flat=True).distinct()

    # Pagination
    paginator = Paginator(cars, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "search_query": search_query,
        "manufacturer_filter": manufacturer_filter,
        "manufacturers": manufacturers,
    }
    return render(request, "racing/cars_list.html", context)


from django.db import models
