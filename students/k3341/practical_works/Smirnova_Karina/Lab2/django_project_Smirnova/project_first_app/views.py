from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import OwnerForm
from .models import Owner, Car
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

def owner_detail(request, owner_id):
    """Метод выводит информации об Автовладельце"""

    try:
        owner = Owner.objects.get(pk=owner_id)
    except Owner.DoesNotExist:
        raise Http404("Owner does not exist")
    return render(request, 'owner.html', {'owner': owner})

def owner_list(request):
    """Функция лдя отображения всех Автовладельцев"""

    context = {"owners": Owner.objects.all()}
    return render(request, "owner_list.html", context)

class CarListView(ListView):
    """Класс для вывода всех автомобилей"""

    model = Car
    template_name = 'car_list.html'

class CarDetailView(DetailView):
    """Класс для вывода информации об автомобиле на id"""
    model = Car
    template_name = 'car_detail.html'

def owner_create_view(request):
    """Функция для создания Автопользователя из формы"""

    form = OwnerForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('owner_create')
    return render(request, "owner_create.html", {"form": form})

class CarCreateView(CreateView):
    """Класс для создания автомобиля"""

    model = Car
    fields = ['state_num', 'brand', 'model', 'color']
    template_name = 'car_form.html'
    success_url = reverse_lazy('car_list')

class CarUpdateView(UpdateView):
    """Класс для обновления автомобиля"""

    model = Car
    fields = ['state_num', 'brand', 'model', 'color']
    template_name = 'car_form.html'
    success_url = reverse_lazy('car_list')

class CarDeleteView(DeleteView):
    """Класс для удаления автомобиля"""

    model = Car
    template_name = 'car_confirm_delete.html'
    success_url = reverse_lazy('car_list')