from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model, login
from .models import Avtomobil, Vladenie
from .forms import AvtomobilForm, UserRegistrationForm

User = get_user_model()


# ========== ФУНКЦИОНАЛЬНЫЕ ПРЕДСТАВЛЕНИЯ ДЛЯ ВЛАДЕЛЬЦЕВ ==========

def owner_list(request):
    """
    Функциональное представление: список всех пользователей-владельцев
    """
    context = {}
    context['owners'] = User.objects.all()
    return render(request, 'owner_list.html', context)


def owner_detail(request, owner_id):
    """
    Функциональное представление: информация о пользователе-владельце
    """
    try:
        owner = User.objects.get(pk=owner_id)
    except User.DoesNotExist:
        raise Http404("Пользователь не найден")
    return render(request, 'owner_detail.html', {'owner': owner})


def owner_create(request):
    """
    Функциональное представление: регистрация нового пользователя-владельца
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            return redirect('owner_list')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'user_registration.html', {'form': form})


# ========== КЛАССОВЫЕ ПРЕДСТАВЛЕНИЯ ДЛЯ АВТОМОБИЛЕЙ ==========

class AvtomobilListView(ListView):
    """
    Классовое представление: список всех автомобилей
    """
    model = Avtomobil
    template_name = 'avtomobil_list.html'
    context_object_name = 'avtomobili'
    
    def get_queryset(self):
        return Avtomobil.objects.all()


class AvtomobilDetailView(DetailView):
    """
    Классовое представление: детальная информация об автомобиле
    """
    model = Avtomobil
    template_name = 'avtomobil_detail.html'
    context_object_name = 'avtomobil'
    pk_url_kwarg = 'avtomobil_id'


class AvtomobilCreateView(CreateView):
    """
    Классовое представление: создание нового автомобиля
    """
    model = Avtomobil
    form_class = AvtomobilForm
    template_name = 'avtomobil_form.html'
    success_url = reverse_lazy('avtomobil_list')


class AvtomobilUpdateView(UpdateView):
    """
    Классовое представление: обновление информации об автомобиле
    """
    model = Avtomobil
    form_class = AvtomobilForm
    template_name = 'avtomobil_form.html'
    success_url = reverse_lazy('avtomobil_list')
    pk_url_kwarg = 'avtomobil_id'


class AvtomobilDeleteView(DeleteView):
    """
    Классовое представление: удаление автомобиля
    """
    model = Avtomobil
    template_name = 'avtomobil_confirm_delete.html'
    success_url = reverse_lazy('avtomobil_list')
    context_object_name = 'avtomobil'
    pk_url_kwarg = 'avtomobil_id'
