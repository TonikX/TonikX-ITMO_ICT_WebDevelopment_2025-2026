from django.shortcuts import render, redirect
from django.contrib.auth import login as _login, logout as _logout
from django.contrib.auth.hashers import make_password
from .forms import UserRegisterForm, UserLoginForm

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save yet, we need to hash the password
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            _login(request, user)
            return redirect("/")
    else:
        if str(request.user) != "AnonymousUser": return redirect("/")
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            _login(request, form.get_user())
            return redirect("/")
    else:
        print(request.user)
        if str(request.user) != "AnonymousUser": return redirect("/")
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    _logout(request)
    return redirect('/accounts/login')