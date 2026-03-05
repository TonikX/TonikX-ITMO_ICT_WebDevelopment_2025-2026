from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView

from race_application.forms import LoginForm, RegisterForm, RacerForm, ReviewForm
from race_application.models import Race, Review, RaceConnection


def user_logout(request):
    logout(request)
    return redirect('races_list')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('profile')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def registration(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "registration.html", {"user_form": form})


@login_required(login_url='/login/')
def dashboard(request):
    if not hasattr(request.user, "racer"):
        return render(request, 'dashboard.html', {'section': 'profile', 'has_racer': hasattr(request.user, 'racer')})
    race_connections = RaceConnection.objects.filter(racer=request.user.racer).values("race")
    racer_races = []
    for race_connection in race_connections:
        try:
            print(race_connection["race"])
            race = Race.objects.get(id=race_connection["race"])
            racer_races.append(race)
        except Race.DoesNotExist:
            continue
    print(racer_races)
    return render(request, 'dashboard.html', {'section': 'profile', 'has_racer': hasattr(request.user, 'racer'), 'races': racer_races})


@login_required(login_url='/login/')
def racer_registration(request):
    user = request.user
    if hasattr(request.user, "racer"):
        return HttpResponse("You have already got a racer")
    else:
        if request.method == "POST":

            racer_form = RacerForm(request.POST)
            if racer_form.is_valid():
                print(user)
                racer = racer_form.save(commit=False)
                racer.user = user
                racer.save()
                user.has_racer = True
                user.save()
                return redirect("profile")
        else:
            racer_form = RacerForm()

    return render(request, "racer_registration.html", {"racer_form": racer_form})


@login_required(login_url='/login/')
def race_reviews(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    reviews = Review.objects.filter(race=race)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.race = race
            review.author = request.user
            review.save()
    else:
        form = ReviewForm()
    return render(request, "race_reviews.html", {"race": race, "reviews": reviews, "form": form})


def races_list(request):
    races = Race.objects.all()
    if not request.user.is_authenticated or not hasattr(request.user, "racer"):
        return render(request, "races_list.html", {"races": races})
    race_connections = RaceConnection.objects.filter(racer=request.user.racer).values("race")
    racer_races = []
    for race_connection in race_connections:
        racer_races.append(race_connection['race'])
    return render(request, "races_list.html", {"races": races, "race_connections": racer_races})



class RacesPivotListView(UserPassesTestMixin, ListView):
    template_name = "races_adm_list.html"
    queryset = Race.objects.all()
    paginate_by = 3
    context_object_name = "races"

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect("races_list")

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        filter_param = self.request.GET.get('filter', '')

        if search_query:
            queryset = queryset.filter(
                Q(id__icontains=search_query) |
                Q(winner__team_name__icontains=search_query) |
                Q(date_of_race__icontains=search_query)
            )

        if filter_param:
            queryset = queryset.filter(status=filter_param)

        return queryset

@login_required(login_url='/login/')
def create_race_connection(request, race_id):
    user = request.user
    if not (hasattr(user, "racer")):
        return HttpResponse("You have not got a racer")
    else:
        try:
            race_connection = RaceConnection()
            race = Race.objects.get(pk=race_id)
            race_connection.race = race
            race_connection.racer = user.racer
            race_connection.save()
        except Exception as ex:
            print(ex)
            return HttpResponse('You have already registrated')
        return redirect("races_list")


def delete_race_connection(request, race_id):
    racer = request.user.racer
    race = Race.objects.get(pk=race_id)
    RaceConnection.objects.filter(racer=racer, race=race).delete()
    return redirect("races_list")