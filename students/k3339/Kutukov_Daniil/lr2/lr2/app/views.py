from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Conference, Registration, Comment
from .forms import UserRegisterForm, RegistrationForm, CommentForm


def conference_list(request):
    """Список конференций с поиском и пагинацией"""
    query = request.GET.get("q", "")
    conferences = Conference.objects.all().order_by("-start_date")

    if query:
        conferences = conferences.filter(
            Q(title__icontains=query)
            | Q(location__title__icontains=query)
            | Q(location__city__title__icontains=query)
            | Q(conditions__icontains=query)
        )

    paginator = Paginator(conferences, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request, "app/conference_list.html", {"page_obj": page_obj, "query": query}
    )


def conference_detail(request, conference_id):
    """Детальная информация о конференции"""
    conference = get_object_or_404(Conference, id=conference_id)
    comments = Comment.objects.filter(conference=conference).order_by("-created_at")
    user_registration = None

    if request.user.is_authenticated:
        user_registration = Registration.objects.filter(
            conference=conference, user=request.user
        ).first()

    return render(
        request,
        "app/conference_detail.html",
        {
            "conference": conference,
            "comments": comments,
            "user_registration": user_registration,
        },
    )


@login_required
def register_for_conference(request, conference_id):
    """Регистрация на конференцию"""
    conference = get_object_or_404(Conference, id=conference_id)

    # Проверяем, не зарегистрирован ли уже пользователь
    existing = Registration.objects.filter(
        conference=conference, user=request.user
    ).first()

    if existing:
        messages.warning(request, "Вы уже зарегистрированы на эту конференцию")
        return redirect("conference_detail", conference_id=conference_id)

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.conference = conference
            registration.user = request.user
            registration.save()
            messages.success(request, "Вы успешно зарегистрировались на конференцию!")
            return redirect("conference_detail", conference_id=conference_id)
    else:
        form = RegistrationForm()

    return render(
        request,
        "app/register_conference.html",
        {"form": form, "conference": conference},
    )


@login_required
def edit_registration(request, registration_id):
    """Редактирование регистрации"""
    registration = get_object_or_404(
        Registration, id=registration_id, user=request.user
    )

    if request.method == "POST":
        form = RegistrationForm(request.POST, instance=registration)
        if form.is_valid():
            form.save()
            messages.success(request, "Регистрация обновлена!")
            return redirect(
                "conference_detail", conference_id=registration.conference.id
            )
    else:
        form = RegistrationForm(instance=registration)

    return render(
        request,
        "app/edit_registration.html",
        {"form": form, "registration": registration},
    )


@login_required
def delete_registration(request, registration_id):
    """Удаление регистрации"""
    registration = get_object_or_404(
        Registration, id=registration_id, user=request.user
    )
    conference_id = registration.conference.id

    if request.method == "POST":
        registration.delete()
        messages.success(request, "Регистрация удалена")
        return redirect("conference_detail", conference_id=conference_id)

    return render(
        request, "app/delete_registration.html", {"registration": registration}
    )


@login_required
def add_comment(request, conference_id):
    """Добавление отзыва к конференции"""
    conference = get_object_or_404(Conference, id=conference_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.conference = conference
            comment.user = request.user
            comment.save()
            messages.success(request, "Отзыв добавлен!")
            return redirect("conference_detail", conference_id=conference_id)
    else:
        form = CommentForm()

    return render(
        request, "app/add_comment.html", {"form": form, "conference": conference}
    )


def participants_table(request):
    """Таблица участников по конференциям с поиском и пагинацией"""
    query = request.GET.get("q", "")
    registrations = Registration.objects.select_related(
        "conference", "user", "conference__location"
    ).order_by("conference__start_date", "user__last_name")

    if query:
        registrations = registrations.filter(
            Q(user__first_name__icontains=query)
            | Q(user__last_name__icontains=query)
            | Q(conference__title__icontains=query)
            | Q(theme__icontains=query)
        )

    paginator = Paginator(registrations, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request, "app/participants_table.html", {"page_obj": page_obj, "query": query}
    )


def register(request):
    """Регистрация нового пользователя"""
    if request.user.is_authenticated:
        return redirect("conference_list")

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация успешна! Добро пожаловать!")
            return redirect("conference_list")
    else:
        form = UserRegisterForm()

    return render(request, "app/register.html", {"form": form})


@login_required
def profile(request):
    """Личный кабинет пользователя"""
    registrations = Registration.objects.filter(user=request.user).select_related(
        "conference"
    )
    comments = Comment.objects.filter(user=request.user).select_related("conference")

    return render(
        request,
        "app/profile.html",
        {"registrations": registrations, "comments": comments},
    )
