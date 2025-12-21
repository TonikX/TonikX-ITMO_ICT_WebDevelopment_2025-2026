from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .forms import OwnerForm, CarForm, OwnershipForm
from .models import Car, Owner, Ownership

def owner_detail(request, id):
    owner = get_object_or_404(Owner, id=id)
    return render(request, 'owner.html', {'owner': owner})

def owner_list(request):
    owners = Owner.objects.all()
    return render(request, 'owners_list.html', {'owners': owners})

def car_list(request):
    cars = Car.objects.all()
    return render(request, 'car_list.html', {'cars': cars})

def car_detail(request, id):
    car = get_object_or_404(Car, id=id)
    owners = Ownership.objects.filter(car=car)
    last_owner = max(owners, key=lambda ownership: ownership.start_date).owner
    return render(request, 'car.html', {'car': car, 'owner': last_owner, 'ownership': owners})

def car_update(request, id):
    car = get_object_or_404(Car, id=id)
    if request.method == 'POST':
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            return redirect('car_detail', id=car.id)
    else:
        form = CarForm(instance=car)
    return render(request, 'car_form.html', {'form': form, 'title': 'Обновить автомобиль'})

def car_delete(request, id):
    car = get_object_or_404(Car, id=id)
    if request.method == 'POST':
        car.delete()
        return redirect('car_list')
    return render(request, 'car_confirm_delete.html', {'car': car})

def owner_create(request):
    if request.method == 'POST':
        form = OwnerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('owner_list')
    else:
        form = OwnerForm()
    return render(request, 'owner_form.html', {'form': form, 'title': 'Добавить человека'})

def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('car_list')
    else:
        form = CarForm()
    
    return render(request, 'add_car.html', {'form': form})

def add_ownership(request):
    if request.method == 'POST':
        form = OwnershipForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ownership_list')
    else:
        form = OwnershipForm()
    
    return render(request, 'add_ownership.html', {'form': form})

def ownership_list(request):
    ownerships = Ownership.objects.select_related('owner', 'car').all()
    return render(request, 'ownership_list.html', {'ownerships': ownerships})

def ownership_detail(request, id):
    car = get_object_or_404(Car, id=id)
    owners = Ownership.objects.filter(car=car)
    ownerships = owners.select_related('owner', 'car').all()
    return render(request, 'ownership_list.html', {'ownerships': ownerships})