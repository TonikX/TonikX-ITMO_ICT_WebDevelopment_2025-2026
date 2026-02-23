from django.shortcuts import render, redirect
from django.http import Http404
from django.urls import reverse_lazy

from project_first_app.models import Owner, Car
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .forms import add_owner
from django.views.generic.edit import UpdateView, CreateView, DeleteView

def owner_information (request, owner_id):
    try:
        owner = Owner.objects.get(pk=owner_id)

    except Owner.DoesNotExist:
        raise Http404("Владелец не найден")

    return render(request, "owner.html", {'owner': owner})


def all_owners(request):
    data = {
        'dataset' : Owner.objects.all()
    }

    return render(request, 'owners.html', context=data)

def create_owner(request):
    if request.method == 'POST':
        form = add_owner(request.POST)
        if form.is_valid():
            form.save()
            return redirect('owners_list')
    else:
        form = add_owner()
    return render(request, 'add_owner.html', {'form': form})


class all_cars(ListView):
    model = Car
    template_name = 'Cars.html'

class one_car(DetailView):
    model = Car
    template_name = 'Car.html'


class update_car(UpdateView):
    model = Car
    template_name = 'car_form.html'
    fields = ['plate_number', 'brand', 'model', 'color']
    success_url = reverse_lazy('cars')


class add_car(CreateView):
    model = Car
    template_name = 'car_form.html'
    fields = ['plate_number', 'brand', 'model', 'color']
    success_url = reverse_lazy('cars')


class delete_car(DeleteView):
    model = Car
    template_name = 'delete_car_form.html'
    success_url = reverse_lazy('cars')








