from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from .models import Owner, Car
from .forms import OwnerForm, CarForm

def home(request):
    return render(request, 'car_app/home.html')

# Функции для владельцев машин
def owner_list(request):
    owners = Owner.objects.all()
    return render(request, 'car_app/owner_list.html', {'owners': owners})

def owner_create(request):
    if request.method == "POST":
        form = OwnerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('owner_list')
    else:
        form = OwnerForm()
    return render(request, 'car_app/owner_form.html', {'form': form})

# Классы для автомобилей
class CarListView(ListView):
    model = Car
    template_name = 'car_app/car_list.html'

class CarDetailView(DetailView):
    model = Car
    template_name = 'car_app/car_detail.html'

class CarCreateView(CreateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy('car_list')
    template_name = 'car_app/car_form.html'

class CarUpdateView(UpdateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy('car_list')
    template_name = 'car_app/car_form.html'

class CarDeleteView(DeleteView):
    model = Car
    success_url = reverse_lazy('car_list')
    template_name = 'car_app/car_confirm_delete.html'