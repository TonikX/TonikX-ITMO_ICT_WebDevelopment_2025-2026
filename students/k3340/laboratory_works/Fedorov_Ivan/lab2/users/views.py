from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib.auth import logout
from django.shortcuts import redirect

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('race_list')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('race_list')

@login_required
def profile(request):
    user_registrations = request.user.raceregistration_set.select_related('race').all()
    user_results = request.user.raceresult_set.select_related('race').all()

    return render(request, 'users/profile.html', {
        'user_registrations': user_registrations,
        'user_results': user_results,
    })