from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import ListView, DetailView

from .forms import UserRegisterForm, ParticipantProfileForm, RegistrationForm, CommentForm
from .models import Race, Registration, ParticipantProfile, Comment

class RaceListView(ListView):
    model = Race
    template_name = "races/race_list.html"
    context_object_name = "races"

class RaceDetailView(DetailView):
    model = Race
    template_name = "races/race_detail.html"
    context_object_name = "race"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        race = ctx["race"]
        user = self.request.user
        reg = None
        if user.is_authenticated and hasattr(user, "participant_profile"):
            reg = Registration.objects.filter(participant=user.participant_profile, race=race).first()
        ctx["user_registration"] = reg
        ctx["registration_form"] = RegistrationForm()
        ctx["comment_form"] = CommentForm()
        return ctx

def register(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        profile_form = ParticipantProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user: User = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data["password"])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            # auto-login
            user = authenticate(username=user.username, password=user_form.cleaned_data["password"])
            if user:
                login(request, user)
            messages.success(request, "Регистрация прошла успешно.")
            return redirect("races:race_list")
    else:
        user_form = UserRegisterForm()
        profile_form = ParticipantProfileForm()
    return render(request, "races/register.html", {"user_form": user_form, "profile_form": profile_form})

@login_required
def profile(request):
    profile = getattr(request.user, "participant_profile", None)
    if request.method == "POST":
        form = ParticipantProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль обновлён.")
            return redirect("races:profile")
    else:
        form = ParticipantProfileForm(instance=profile)
    return render(request, "races/profile.html", {"form": form})

@login_required
def create_registration(request, pk):
    race = get_object_or_404(Race, pk=pk)
    if request.method == "POST":
        if not hasattr(request.user, "participant_profile"):
            messages.error(request, "Создайте профиль участника.")
            return redirect("races:profile")
        participant = request.user.participant_profile
        reg, created = Registration.objects.get_or_create(participant=participant, race=race)
        if created:
            messages.success(request, "Вы зарегистрированы на гонку.")
        else:
            messages.info(request, "Вы уже зарегистрированы на эту гонку.")
        return redirect("races:race_detail", pk=race.pk)
    raise Http404()

@login_required
def delete_registration(request, pk):
    reg = get_object_or_404(Registration, pk=pk)
    if not hasattr(request.user, "participant_profile") or reg.participant != request.user.participant_profile:
        return HttpResponseForbidden("Можно удалять только свою регистрацию.")
    race_id = reg.race_id
    reg.delete()
    messages.success(request, "Регистрация удалена.")
    return redirect("races:race_detail", pk=race_id)

@login_required
def create_comment(request, pk):
    race = get_object_or_404(Race, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.race = race
            comment.author = request.user
            comment.save()
            messages.success(request, "Комментарий добавлен.")
            return redirect("races:race_detail", pk=race.pk)
    return redirect("races:race_detail", pk=race.pk)
