from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Car, Owner, Ownership


def owner_list(request):
    context = {
        'owners': Owner.objects.all(),
    }
    return render(request, 'owner_list.html', context)


def owner_detail(request, owner_id):
    owner = Owner.objects.get(id=owner_id)
    ownerships = Ownership.objects.filter(owner=owner)
    context = {
        'owner': owner,
        'ownerships': ownerships,
    }
    return render(request, 'owner_detail.html', context)


class CarListView(ListView):
    model = Car
    template_name = 'car_list.html'
    context_object_name = 'cars'


class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'
    context_object_name = 'car'


class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_confirm_delete.html'
    success_url = reverse_lazy('car_list')
