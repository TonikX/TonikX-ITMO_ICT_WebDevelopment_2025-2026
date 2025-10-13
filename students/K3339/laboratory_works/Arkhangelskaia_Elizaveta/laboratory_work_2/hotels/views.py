from django.shortcuts import render, redirect
from .forms import HotelUserCreationForm

def register(request):
    if request.method == "POST":
        form = HotelUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Перенаправляем на страницу логина
    else:
        form = HotelUserCreationForm()
    return render(request, 'register.html', {'form': form})

