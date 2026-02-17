from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import CarOwner, Car
from .forms import CarOwnerForm, CarForm


def owner_list(request):
    owners = CarOwner.objects.all()
    return render(request, 'owner_list.html', {'owners': owners})


def owner_detail(request, owner_id):
    try:
        owner = CarOwner.objects.get(pk=owner_id)
    except CarOwner.DoesNotExist:
        raise Http404("Owner not found")
    return render(request, 'owner.html', {'owner': owner})


def owner_create(request):
    if request.method == 'POST':
        form = CarOwnerForm(request.POST)
        if form.is_valid():
            owner = form.save(commit=False)
            owner.set_password(form.cleaned_data['password'])
            owner.save()
            return redirect('owner_list')
    else:
        form = CarOwnerForm()
    return render(request, 'owner_form.html', {'form': form})


class CarListView(ListView):
    model = Car
    template_name = 'car_list.html'
    context_object_name = 'cars'


class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'
    context_object_name = 'car'


class CarCreateView(CreateView):
    model = Car
    form_class = CarForm
    template_name = 'car_form.html'
    success_url = '/cars/'


class CarUpdateView(UpdateView):
    model = Car
    form_class = CarForm
    template_name = 'car_form.html'
    success_url = '/cars/'


class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_confirm_delete.html'
    success_url = '/cars/'
