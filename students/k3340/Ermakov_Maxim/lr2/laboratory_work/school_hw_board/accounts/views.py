from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import StudentSignUpForm
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views.decorators.http import require_http_methods

def signup(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homework_list')
    else:
        form = StudentSignUpForm()
    return render(request, 'accounts/signup.html', {"form": form})


@require_http_methods(["GET", "POST"])
def logout_view(request):
    logout(request)
    return redirect('login')  # всегда уводим на /accounts/login/