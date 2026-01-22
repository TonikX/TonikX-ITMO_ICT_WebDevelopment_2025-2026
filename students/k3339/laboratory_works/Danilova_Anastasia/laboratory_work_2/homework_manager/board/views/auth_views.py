# views/auth_views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from ..forms import RegisterForm, LoginForm
from ..utils import redirect_user_by_role


def signup_view(request):
    """New user's registration"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect_user_by_role(user)
        else:
            print(form.errors)
    else:
        form = RegisterForm()

    context = {
        'form': form,
        'user': request.user,
    }
    return render(request, 'board/register.html', context)


def login_view(request):
    """User's login page"""
    form = LoginForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect_user_by_role(user)

    context = {
        'form': form,
        'user': request.user,
    }
    return render(request, 'board/login.html', context)