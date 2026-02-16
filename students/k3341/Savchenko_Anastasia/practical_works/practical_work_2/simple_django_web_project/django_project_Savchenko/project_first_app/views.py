from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import CarOwner, Car, Ownership, DriversLicense
import datetime

# импорты для классовых представлений
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from .forms import CarOwnerForm, CarForm  # импортируем обе формы


# функция для детальной инфы о владельце - осталась с  2.1
def owner_detail(request, owner_id):
    try:
        owner = CarOwner.objects.get(pk=owner_id)
    except CarOwner.DoesNotExist:
        raise Http404("Владелец не найден")

    return render(request, 'owner.html', {'owner': owner})


# список всех владельцев - функциональное представление
def owner_list(request):
    owners = CarOwner.objects.all()
    context = {
        'owners': owners,
        'current_time': datetime.datetime.now(),
    }
    return render(request, 'owner_list.html', context)


# пример из задания - вывод времени без шаблона
def example_view(request):
    now = datetime.datetime.now()
    html = f"Time is {now}"
    return HttpResponse(html)


# ============================================================================
# КЛАССОВЫЕ ПРЕДСТАВЛЕНИЯ ДЛЯ АВТОМОБИЛЕЙ    задаание 2.2
# ============================================================================

# класс для списка всех автомобилей
class CarListView(ListView):
    # модель, с которой работаем
    model = Car
    # шаблон для отображения
    template_name = 'car_list.html'
    # как называть список объектов в шаблоне
    context_object_name = 'cars'

    # можно добавить что-то в контекст
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # общее количество авто - пригодится в шаблоне
        context['car_count'] = Car.objects.count()
        return context


# класс для детальной информации об одном автомобиле
class CarDetailView(DetailView):
    # модель та же
    model = Car
    # свой шаблон
    template_name = 'car_detail.html'
    # как называть объект в шаблоне
    context_object_name = 'car'

    # добавляем владельцев в контекст
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.get_object()  # текущий автомобиль

        # все владельцы этого авто
        context['owners'] = car.owners.all()
        # вся история владения
        context['ownerships'] = car.ownerships.all()

        return context


# класс для редактирования автомобиля
# class CarUpdateView(UpdateView):
#     model = Car
#     template_name = 'car_form.html'
#     # какие поля можно менять
#     fields = ['state_number', 'brand', 'model', 'color']
#     # куда переходить после сохранения
#     success_url = reverse_lazy('car_list')
class CarUpdateView(UpdateView):
    """Обновление информации об автомобиле"""
    model = Car
    template_name = 'car_form.html'
    # используем нашу форму вместо указания полей
    form_class = CarForm
    # куда перенаправлять после успешного обновления
    success_url = reverse_lazy('car_list')

# ============================================================================
# 2.2 Практическое задание (по задаче 3)  ФОРМЫ ДЛЯ ВЛАДЕЛЬЦЕВ (функциональные представления)
# ============================================================================
# 1. Реализовать форму ввода всех владельцев функционально. Добавить данные минимум о еще трех владельцах. Должны быть реализованы форма (Form), контроллер (views) и шаблоны (temlates).
def create_owner(request):
    """
    Создание нового владельца через форму.
    Работает так:
    1. При GET-запросе показывает пустую форму
    2. При POST-запросе проверяет данные и сохраняет владельца
    """
    # если форма была отправлена (пользователь нажал "Сохранить")
    if request.method == 'POST':
        # создаем форму с данными из запроса
        form = CarOwnerForm(request.POST)

        # проверяем, все ли поля заполнены правильно
        if form.is_valid():
            # сохраняем нового владельца в базу
            form.save()

            # после сохранения перенаправляем на список владельцев
            # можно показать сообщение об успехе, но для простоты просто редирект
            return render(request, 'owner_create_success.html', {
                'owner': form.instance  # только что созданный владелец
            })

    # если это GET-запрос (просто открыли страницу)
    else:
        # создаем пустую форму
        form = CarOwnerForm()

    # передаем форму в шаблон
    return render(request, 'owner_form.html', {'form': form})


# ============================================================================
# КЛАССЫ ДЛЯ СОЗДАНИЯ И УДАЛЕНИЯ АВТОМОБИЛЕЙ
# ============================================================================

class CarCreateView(CreateView):
    """Создание нового автомобиля"""
    model = Car
    template_name = 'car_create_form.html'  # отдельный шаблон для создания
    form_class = CarForm  # используем ту же форму
    # после создания переходим к списку автомобилей
    success_url = reverse_lazy('car_list')

    # можно добавить дополнительный контекст
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить новый автомобиль'
        return context


class CarDeleteView(DeleteView):
    """Удаление автомобиля"""
    model = Car
    template_name = 'car_confirm_delete.html'  # шаблон подтверждения удаления
    # после удаления переходим к списку автомобилей
    success_url = reverse_lazy('car_list')

    # можно добавить дополнительный контекст
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление автомобиля'
        return context