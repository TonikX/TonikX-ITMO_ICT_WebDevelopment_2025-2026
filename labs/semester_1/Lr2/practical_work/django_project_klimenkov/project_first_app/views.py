from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from .models import Owner, Car
from .forms import OwnerForm


def root_redirect(request):
    return redirect('owners_list')


def owners_list(request):
    """
    Представление для отображения списка всех владельцев автомобилей.
    """
    owners = Owner.objects.all()
    return render(request, 'owners/owners_list.html', {'owners': owners})


def owner_detail(request, id):
    """
    Представление для отображения детальной информации об автовладельце.
    """
    try:
        owner = Owner.objects.get(pk=id)
    except Owner.DoesNotExist:
        raise Http404("Автовладелец не найден")
    
    return render(request, 'owners/owner_detail.html', {'owner': owner})


def create_owner(request):
    if request.method == 'POST':
        form = OwnerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('owners_list')
    else:
        form = OwnerForm()
    return render(request, 'owners/create_owner.html', {'form': form})


def edit_owner(request, id):
    owner = get_object_or_404(Owner, id=id)
    if request.method == 'POST':
        form = OwnerForm(request.POST, instance=owner)
        if form.is_valid():
            form.save()
            return redirect('owners_list')
    else:
        form = OwnerForm(instance=owner)
    return render(request, 'owners/edit_owner.html', {'form': form, 'owner': owner})


def delete_owner(request, id):
    owner = get_object_or_404(Owner, id=id)
    if request.method == 'POST':
        owner.delete()
        return redirect('owners_list')
    return render(request, 'owners/confirm_delete_owner.html', {'owner': owner})


class CarsListView(ListView):
    model = Car
    template_name = 'cars/cars_list.html'
    context_object_name = 'cars'


class CarDetailView(DetailView):
    model = Car
    template_name = 'cars/car_detail.html'
    context_object_name = 'car'
    pk_url_kwarg = 'car_id'


class CarCreateView(CreateView):
    model = Car
    template_name = 'cars/create_car.html'
    fields = ['license_plate', 'model', 'color']
    success_url = reverse_lazy('cars_list')


class CarUpdateView(UpdateView):
    model = Car
    template_name = 'cars/edit_car.html'
    fields = ['license_plate', 'model', 'color']
    success_url = reverse_lazy('cars_list')
    context_object_name = 'car'
    pk_url_kwarg = 'car_id'


class CarDeleteView(DeleteView):
    model = Car
    template_name = 'cars/confirm_delete_car.html'
    success_url = reverse_lazy('cars_list')
    context_object_name = 'car'
    pk_url_kwarg = 'car_id'
