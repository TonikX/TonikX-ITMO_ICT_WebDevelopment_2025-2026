from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import User, Car, Ownership, DriverLicense
from django.contrib.auth import get_user_model

User = get_user_model()

def user_detail(request, user_id):
    """
    Отображает информацию о пользователе (владельце автомобиля) по его ID.
    """
    user = get_object_or_404(User, pk=user_id)

    # Получаем связанные автомобили и водительские удостоверения
    cars = user.ownerships.all()
    licenses = user.licenses.all()

    context = {
        'user': user,
        'cars': cars,
        'licenses': licenses,
    }

    return render(request, 'user_detail.html', context)


def user_list(request):
    users = User.objects.all()
    return render(request, 'owners/owner_list.html', {'users': users})

'''
from django.shortcuts import render, redirect
from .forms import OwnerForm

def owner_create(request):
    if request.method == 'POST':
        form = OwnerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('owner_list')
    else:
        form = OwnerForm()
    return render(request, 'owners/owner_form.html', {'form': form})
'''
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm

def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'owners/user_register.html', {'form': form})


from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy

class CarListView(ListView):
    model = Car
    template_name = 'cars/car_list.html'
    context_object_name = 'cars'

class CarDetailView(DetailView):
    model = Car
    template_name = 'cars/car_detail.html'
    context_object_name = 'car'

class CarUpdateView(UpdateView):
    model = Car
    fields = ['plate_number', 'brand', 'model', 'color']
    template_name = 'cars/car_form.html'
    success_url = reverse_lazy('car_list')


class CarCreateView(CreateView):
    model = Car
    fields = ['plate_number', 'brand', 'model', 'color']
    template_name = 'cars/car_form.html'
    success_url = reverse_lazy('car_list')

class CarDeleteView(DeleteView):
    model = Car
    template_name = 'cars/car_confirm_delete.html'
    success_url = reverse_lazy('car_list')