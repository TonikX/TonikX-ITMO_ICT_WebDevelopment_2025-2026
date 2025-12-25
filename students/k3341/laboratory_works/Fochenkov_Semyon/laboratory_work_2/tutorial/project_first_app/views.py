from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import User, Car, Ownership, DriverLicense
from .forms import OwnerForm, DriverLicenseForm


def home(request):
    """Главная страница с информацией о проекте"""
    owners_count = User.objects.count()
    cars_count = Car.objects.count()
    ownerships_count = Ownership.objects.count()
    licenses_count = DriverLicense.objects.count()
    
    owners = User.objects.all()[:5] 
    
    context = {
        'owners_count': owners_count,
        'cars_count': cars_count,
        'ownerships_count': ownerships_count,
        'licenses_count': licenses_count,
        'owners': owners,
    }
    return render(request, 'home.html', context)


def owners_list(request):
    """Функциональное представление для вывода всех владельцев"""
    context = {}
    context["dataset"] = User.objects.all()
    return render(request, "owners_list.html", context)


def owner_detail(request, owner_id):
    """Контроллер для отображения детальной информации о владельце"""
    try:
        owner = User.objects.get(pk=owner_id)
        ownerships = Ownership.objects.filter(owner=owner).select_related('car')
        licenses = DriverLicense.objects.filter(owner=owner)
    except User.DoesNotExist:
        raise Http404("Владелец не найден")
    
    context = {
        'owner': owner,
        'ownerships': ownerships,
        'licenses': licenses,
    }
    return render(request, 'owner.html', context)


# Классовые представления для автомобилей
class CarListView(ListView):
    """Классовое представление для вывода списка автомобилей"""
    model = Car
    template_name = 'car_list.html'
    context_object_name = 'cars'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список автомобилей'
        return context


class CarDetailView(DetailView):
    """Классовое представление для вывода детальной информации об автомобиле"""
    model = Car
    template_name = 'car_detail.html'
    context_object_name = 'car'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.get_object()
        ownerships = Ownership.objects.filter(car=car).select_related('owner')
        context['ownerships'] = ownerships
        return context


class CarCreateView(CreateView):
    """Классовое представление для создания автомобиля"""
    model = Car
    fields = ['brand', 'model', 'color', 'state_number']
    template_name = 'car_form.html'
    success_url = '/cars/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить автомобиль'
        context['action'] = 'create'
        return context


class CarUpdateView(UpdateView):
    """Классовое представление для обновления автомобиля"""
    model = Car
    fields = ['brand', 'model', 'color', 'state_number']
    template_name = 'car_form.html'
    success_url = '/cars/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать автомобиль'
        context['action'] = 'update'
        return context


class CarDeleteView(DeleteView):
    """Классовое представление для удаления автомобиля"""
    model = Car
    template_name = 'car_confirm_delete.html'
    success_url = '/cars/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удалить автомобиль'
        return context


# Функциональные представления для владельцев
def owner_create(request):
    """Функциональное представление для создания владельца"""
    if request.method == 'POST':
        form = OwnerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Владелец успешно создан!')
            return redirect('owners_list')
    else:
        form = OwnerForm()
    
    context = {
        'form': form,
        'title': 'Добавить владельца',
        'action': 'create'
    }
    return render(request, 'owner_form.html', context)


def owner_update(request, owner_id):
    """Функциональное представление для обновления владельца"""
    owner = get_object_or_404(User, id=owner_id)
    
    if request.method == 'POST':
        form = OwnerForm(request.POST, instance=owner)
        if form.is_valid():
            form.save()
            messages.success(request, 'Владелец успешно обновлен!')
            return redirect('owner_detail', owner_id=owner.id)
    else:
        form = OwnerForm(instance=owner)
    
    context = {
        'form': form,
        'owner': owner,
        'title': 'Редактировать владельца',
        'action': 'update'
    }
    return render(request, 'owner_form.html', context)


def owner_delete(request, owner_id):
    """Функциональное представление для удаления владельца"""
    owner = get_object_or_404(User, id=owner_id)
    
    if request.method == 'POST':
        owner.delete()
        messages.success(request, 'Владелец успешно удален!')
        return redirect('owners_list')
    
    context = {
        'owner': owner,
        'title': 'Удалить владельца'
    }
    return render(request, 'owner_confirm_delete.html', context)


# Представления для аутентификации
def register(request):
    """Регистрация нового пользователя-владельца"""
    if request.method == 'POST':
        form = OwnerForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.first_name}! Регистрация прошла успешно.')
            return redirect('home')
    else:
        form = OwnerForm()
    
    context = {
        'form': form,
        'title': 'Регистрация владельца автомобиля',
        'action': 'register'
    }
    return render(request, 'register.html', context)


@login_required
def profile(request):
    """Профиль текущего пользователя"""
    user = request.user
    ownerships = Ownership.objects.filter(owner=user).select_related('car')
    licenses = DriverLicense.objects.filter(owner=user)
    
    context = {
        'user': user,
        'ownerships': ownerships,
        'licenses': licenses,
    }
    return render(request, 'profile.html', context)
