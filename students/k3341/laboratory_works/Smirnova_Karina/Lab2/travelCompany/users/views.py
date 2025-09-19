from django.contrib.auth import login
from django.shortcuts import render, redirect

from students.k3341.laboratory_works.Smirnova_Karina.Lab2.travelCompany.users.forms import UserRegisterForm


def register_view(request):
    """Функция для регистрации пользователя"""
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

