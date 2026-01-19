from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from .models import Owner, Car
from .forms import OwnerForm, CarForm

def owners_list(request):
    owners = Owner.objects.all().order_by('last_name', 'first_name')
    return render(request, 'owners_list.html', {'owners': owners})


def owner_detail(request, owner_id: int):
    owner = get_object_or_404(Owner, pk=owner_id)
    ownerships = owner.ownership_set.select_related('car').order_by('-date_start')
    return render(request, 'owner.html', {'owner': owner, 'ownerships': ownerships})


def owner_create(request):
    if request.method == "POST":
        form = OwnerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("owners_list")
    else:
        form = OwnerForm()
    return render(request, "owner_create.html", {"form": form})

class CarCreateView(CreateView):
    model = Car
    form_class = CarForm
    template_name = 'car_form.html'
    success_url = reverse_lazy('car-list')

class CarListView(ListView):
    model = Car
    template_name = 'car_list.html'
    context_object_name = 'cars'
    paginate_by = 20

class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'
    context_object_name = 'car'

class CarUpdateView(UpdateView):
    model = Car
    form_class = CarForm
    template_name = 'car_form.html'
    success_url = reverse_lazy('car-list')

class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_confirm_delete.html'
    success_url = reverse_lazy('car-list')