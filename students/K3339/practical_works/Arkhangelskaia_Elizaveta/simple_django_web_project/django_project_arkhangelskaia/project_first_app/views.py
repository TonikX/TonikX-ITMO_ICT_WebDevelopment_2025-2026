from django.views.generic import ListView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from .models import Car
from .forms import OwnershipForm, CarForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView



def owner_list(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    owners = car.owners.all()

    return render(request,
                  'owner_list.html',
                  {'car': car, 'owners': owners})


class CarListView(ListView):
    model = Car
    template_name = 'car_list.html'
    context_object_name = 'cars'


class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'
    context_object_name = 'car'

class CarUpdateView(UpdateView):
    model = Car
    fields = ['number', 'car_brand', 'car_model', 'car_color']
    template_name = 'car_update.html'
    success_url = reverse_lazy('car_list')



def add_owner_to_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == "POST":
        form = OwnershipForm(request.POST)
        if form.is_valid():
            ownership = form.save(commit=False)
            ownership.id_car = car
            ownership.save()
            return redirect('owner_list', car_id=car.id)
    else:
        form = OwnershipForm()

    return render(request, 'add_owner.html', {'car': car, 'form': form})


class CarCreateView(CreateView):
    model = Car
    form_class = CarForm
    template_name = 'car_form.html'
    success_url = reverse_lazy('car_list')

class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_confirm_delete.html'
    success_url = reverse_lazy('car_list')