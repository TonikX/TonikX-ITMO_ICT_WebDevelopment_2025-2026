from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
from conferences.models import Registration, Review


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Аккаунт создан. Теперь войдите.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    # все заявки пользователя, новые сверху
    regs = (
        Registration.objects
        .filter(user=request.user)
        .select_related("conference", "conference__place")
        .order_by("-created")
    )

    # все отзывы пользователя, новые сверху
    reviews = (
        Review.objects
        .filter(user=request.user)
        .select_related("conference")
        .order_by("-date_posted")
    )

    return render(
        request,
        "users/profile.html",
        {
            "regs": regs,
            "reviews": reviews,
        },
    )
