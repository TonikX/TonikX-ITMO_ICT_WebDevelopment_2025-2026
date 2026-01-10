from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
import logging
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Car
from .forms import OwnerCreationForm
from django.db import models

User = get_user_model()


def owner_detail(request, owner_id):
    """
    Представление для отображения информации о владельце автомобиля по ID
    """
    try:
        owner = User.objects.get(pk=owner_id)
    except User.DoesNotExist:
        raise Http404("Владелец автомобиля не найден")
    
    return render(request, 'owner.html', {'owner': owner})


def owner_list(request):
    """
    Функциональное представление для вывода всех владельцев
    """
    q = request.GET.get('q', '').strip()
    page = request.GET.get('page', 1)

    qs = User.objects.all().order_by('last_name', 'first_name')
    if q:
        qs = qs.filter(
            models.Q(first_name__icontains=q) |
            models.Q(last_name__icontains=q) |
            models.Q(username__icontains=q) |
            models.Q(passport_number__icontains=q)
        )

    paginator = Paginator(qs, 5)  # 5 items per page
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'dataset': page_obj.object_list,
        'paginator': paginator,
        'page_obj': page_obj,
    }
    return render(request, "owner_list.html", context)


def create_owner(request):
    """
    Функциональное представление для создания владельца автомобиля
    """
    context = {}
    form = OwnerCreationForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Владелец успешно создан')
        return redirect('owner_list')

    # Log form errors for debugging and show a message
    if form.errors:
        logging.getLogger(__name__).warning('OwnerCreationForm errors: %s', form.errors.as_json())
        messages.error(request, 'Форма содержит ошибки — проверьте поля ниже.')

    context['form'] = form
    return render(request, "owner_create.html", context)


class CarListView(ListView):
    """
    Представление на основе класса для вывода списка всех автомобилей
    """
    model = Car
    template_name = 'car_list.html'
    context_object_name = 'cars'


class CarDetailView(DetailView):
    """
    Представление на основе класса для вывода информации об автомобиле по ID
    """
    model = Car
    template_name = 'project_first_app/car_detail.html'
    context_object_name = 'car'
    pk_url_kwarg = 'car_id'


class CarCreateView(CreateView):
    """
    Представление на основе класса для создания автомобиля
    """
    model = Car
    template_name = 'project_first_app/car_create.html'
    fields = ['plate_number', 'brand', 'model', 'color']
    success_url = reverse_lazy('car_list')


class CarUpdateView(UpdateView):
    """
    Представление на основе класса для обновления информации об автомобиле
    """
    model = Car
    template_name = 'project_first_app/car_update.html'
    fields = ['plate_number', 'brand', 'model', 'color']
    pk_url_kwarg = 'car_id'
    success_url = reverse_lazy('car_list')


class CarDeleteView(DeleteView):
    """
    Представление на основе класса для удаления автомобиля
    """
    model = Car
    template_name = 'project_first_app/car_delete.html'
    pk_url_kwarg = 'car_id'
    success_url = reverse_lazy('car_list')
