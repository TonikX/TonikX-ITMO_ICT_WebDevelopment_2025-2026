from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from .models import Owner, Car
from .forms import OwnerForm
import datetime

def health_check(request):
    return HttpResponse("OK", content_type="text/plain")

def current_time(request):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return HttpResponse(f"<h2>Текущее время сервера:</h2><p>{now}</p>")

def owner_detail(request, owner_id):
    try:
        owner = Owner.objects.get(pk=owner_id)
    except Owner.DoesNotExist:
        raise Http404("Владелец не найден")

    return render(request, 'owner.html', {'owner': owner})

def owner_list(request):
    owners = Owner.objects.all()
    return render(request, 'owner_list.html', {'owners': owners})

def owner_create(request):
    if request.method == 'POST':
        form = OwnerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('owner_list')
    else:
        form = OwnerForm()
    return render(request, 'owner_form.html', {'form': form})

class CarListView(ListView):
    model = Car
    template_name = 'project_first_app/car_list.html'
    context_object_name = 'cars'
    paginate_by = 10


class CarDetailView(DetailView):
    model = Car
    template_name = 'project_first_app/car_detail.html'
    context_object_name = 'car'


class CarUpdateView(UpdateView):
    model = Car
    fields = ['plate_number', 'make', 'model', 'color']
    template_name = 'project_first_app/car_form.html'
    success_url = reverse_lazy('car_list')

class CarCreateView(CreateView):
    model = Car
    fields = ['plate_number', 'make', 'model', 'color']
    template_name = 'project_first_app/car_form.html'
    success_url = reverse_lazy('car_list')

class CarDeleteView(DeleteView):
    model = Car
    template_name = 'project_first_app/car_confirm_delete.html'
    success_url = reverse_lazy('car_list')