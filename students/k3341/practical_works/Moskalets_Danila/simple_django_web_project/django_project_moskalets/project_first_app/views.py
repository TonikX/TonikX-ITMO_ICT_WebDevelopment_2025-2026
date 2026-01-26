from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import CarOwnerForm, OwnershipForm, CarUserCreationForm
from .models import *


def owners_list(request):
    owners = CarUser.objects.all()

    return render(request, 'project_first_app/owners_list.html', context={'owners': owners})


def owner_detail(request, owner_id):
    owner = get_object_or_404(CarOwner, id_owner=owner_id)

    ownerships = Ownership.objects.filter(
        id_owner=owner
    ).select_related('id_car').order_by('-start_date')

    try:
        license = DriverLicense.objects.get(id_owner=owner)
    except DriverLicense.DoesNotExist:
        license = None

    total_cars = ownerships.count()
    current_cars = ownerships.filter(end_date__isnull=True).count()
    past_cars = ownerships.filter(end_date__isnull=False).count()

    context = {
        'owner': owner,
        'ownerships': ownerships,
        'license': license,
        'total_cars': total_cars,
        'current_cars': current_cars,
        'past_cars': past_cars,
    }

    return render(request, 'project_first_app/owner_detail.html', context)


def owners_create(request):
    context = {}

    form = CarOwnerForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect(reverse('owners_list_url'))

    context['form'] = form
    return render(request, "project_first_app/owners_create.html", context)


class CarsListView(ListView):
    model = Car
    template_name = 'project_first_app/cars_list.html'


class CarsDetailView(DetailView):
    model = Car
    template_name = 'project_first_app/car_detail.html'


class CarFormMixin:
    fields = ['license_plate', 'brand', 'model', 'color']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['license_plate'].widget.attrs.update({'class': 'form-control'})
        form.fields['brand'].widget.attrs.update({'class': 'form-control'})
        form.fields['model'].widget.attrs.update({'class': 'form-control'})
        form.fields['color'].widget.attrs.update({'class': 'form-control'})
        return form


class CarsCreateView(CarFormMixin, CreateView):
    model = Car
    template_name = 'project_first_app/cars_create.html'
    success_url = reverse_lazy('cars_list_url')


class CarUpdateView(CarFormMixin, UpdateView):
    model = Car
    template_name = 'project_first_app/cars_create.html'

    def get_success_url(self):
        return reverse('car_detail', kwargs={'pk': self.object.id})


class CarDeleteView(DeleteView):
    model = Car
    template_name = 'project_first_app/car_delete.html'
    success_url = reverse_lazy('cars_list_url')


class OwnershipCreateView(CreateView):
    model = Ownership
    form_class = OwnershipForm
    template_name = 'project_first_app/ownership_create.html'
    success_url = reverse_lazy('owners_list_url')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form


class CarUserCreateView(CreateView):
    model = CarUser
    form_class = CarUserCreationForm
    template_name = 'project_first_app/caruser_create.html'
    success_url = reverse_lazy('owners_list_url')