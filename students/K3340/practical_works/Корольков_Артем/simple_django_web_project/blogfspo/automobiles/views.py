# automobiles/views.py

from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.db.models import Q
from .models import Owner, Car, Ownership, DriverLicense
from django.shortcuts import render, redirect, get_object_or_404
from .forms import OwnerForm, DriverLicenseForm, OwnershipForm
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages


def owner_detail(request, owner_id):
    """
    Контроллер для отображения детальной информации о владельце
    """
    try:
        # Получаем владельца по ID
        owner = Owner.objects.get(pk=owner_id)

        # Получаем все записи о владении автомобилями для этого владельца
        ownerships = Ownership.objects.filter(owner=owner).select_related('car').order_by('-start_date')

        # Получаем водительские удостоверения владельца
        licenses = DriverLicense.objects.filter(owner=owner)

    except Owner.DoesNotExist:
        raise Http404("Владелец не найден")

    # Передаем данные в шаблон
    return render(request, 'owner.html', {
        'owner': owner,
        'ownerships': ownerships,
        'licenses': licenses
    })


def car_detail(request, car_id):
    """
    Новый контроллер для отображения информации об автомобиле
    """
    try:
        car = Car.objects.get(pk=car_id)
        ownerships = Ownership.objects.filter(car=car).select_related('owner').order_by('-start_date')
    except Car.DoesNotExist:
        raise Http404("Автомобиль не найден")

    return render(request, 'car.html', {
        'car': car,
        'ownerships': ownerships
    })


def owners_list(request):
    """Список всех владельцев с дополнительной информацией"""
    owners = Owner.objects.all().prefetch_related('ownerships__car', 'licenses')

    # Добавляем дополнительную информацию для каждого владельца
    owners_with_info = []
    for owner in owners:
        # Текущие автомобили (без даты окончания владения)
        current_cars = owner.ownerships.filter(end_date__isnull=True).select_related('car')
        # Все автомобили в истории
        all_cars_count = owner.ownerships.count()
        # Водительские удостоверения
        licenses = owner.licenses.all()

        owners_with_info.append({
            'owner': owner,
            'current_cars': current_cars,
            'all_cars_count': all_cars_count,
            'licenses': licenses
        })

    return render(request, 'owners_list.html', {
        'owners_with_info': owners_with_info
    })

def cars_list(request):
    """Список всех автомобилей"""
    cars = Car.objects.all()
    return render(request, 'cars_list.html', {'cars': cars})





def owner_create(request):
    """Создание нового владельца"""
    if request.method == 'POST':
        form = OwnerForm(request.POST)
        if form.is_valid():
            owner = form.save()
            messages.success(request, f'Владелец {owner.get_full_name()} успешно создан!')
            return redirect('owner_detail', owner_id=owner.id)
    else:
        form = OwnerForm()

    return render(request, 'owner_form.html', {
        'form': form,
        'title': 'Добавление нового владельца',
        'submit_text': 'Создать владельца'
    })


def owner_update(request, owner_id):
    """Редактирование владельца"""
    owner = get_object_or_404(Owner, id=owner_id)

    if request.method == 'POST':
        form = OwnerForm(request.POST, instance=owner)
        if form.is_valid():
            owner = form.save()
            messages.success(request, f'Данные владельца {owner.get_full_name()} успешно обновлены!')
            return redirect('owner_detail', owner_id=owner.id)
    else:
        form = OwnerForm(instance=owner)

    return render(request, 'owner_form.html', {
        'form': form,
        'title': f'Редактирование владельца: {owner.get_full_name()}',
        'submit_text': 'Сохранить изменения'
    })


def owner_delete(request, owner_id):
    """Удаление владельца"""
    owner = get_object_or_404(Owner, id=owner_id)

    if request.method == 'POST':
        owner_name = owner.get_full_name()
        owner.delete()
        messages.success(request, f'Владелец {owner_name} успешно удален!')
        return redirect('owners_list')

    return render(request, 'owner_confirm_delete.html', {
        'owner': owner
    })


def add_license(request, owner_id):
    """Добавление водительского удостоверения"""
    owner = get_object_or_404(Owner, id=owner_id)

    if request.method == 'POST':
        form = DriverLicenseForm(request.POST)
        if form.is_valid():
            license_obj = form.save(commit=False)
            license_obj.owner = owner
            license_obj.save()
            messages.success(request, f'Водительское удостоверение {license_obj.license_number} добавлено!')
            return redirect('owner_detail', owner_id=owner.id)
    else:
        form = DriverLicenseForm()

    return render(request, 'license_form.html', {
        'form': form,
        'owner': owner,
        'title': f'Добавление удостоверения для {owner.get_full_name()}'
    })


def add_ownership(request, owner_id):
    """Добавление автомобиля владельцу"""
    owner = get_object_or_404(Owner, id=owner_id)

    if request.method == 'POST':
        form = OwnershipForm(request.POST)
        if form.is_valid():
            ownership = form.save(commit=False)
            ownership.owner = owner
            ownership.save()
            messages.success(request, f'Автомобиль {ownership.car} добавлен владельцу!')
            return redirect('owner_detail', owner_id=owner.id)
    else:
        form = OwnershipForm()

    return render(request, 'ownership_form.html', {
        'form': form,
        'owner': owner,
        'title': f'Добавление автомобиля для {owner.get_full_name()}'
    })



# Классы для автомобилей
class CarListView(ListView):
    """Класс-представление для списка автомобилей"""
    model = Car
    template_name = 'cars_list_class.html'
    context_object_name = 'cars'

    def get_queryset(self):
        """Оптимизируем запрос с предзагрузкой связанных данных"""
        try:
            return Car.objects.prefetch_related('ownerships__owner').all()
        except Exception as e:
            print(f"Ошибка при получении автомобилей: {e}")
            return Car.objects.all()

    def get_context_data(self, **kwargs):
        """Добавляем дополнительный контекст"""
        context = super().get_context_data(**kwargs)
        try:
            context['total_cars'] = self.get_queryset().count()
        except Exception as e:
            print(f"Ошибка при подсчете автомобилей: {e}")
            context['total_cars'] = 0
        return context


class CarDetailView(DetailView):
    """Класс-представление для детальной информации об автомобиле"""
    model = Car
    template_name = 'car_detail_class.html'
    context_object_name = 'car'

    def get_context_data(self, **kwargs):
        """Добавляем историю владения в контекст"""
        context = super().get_context_data(**kwargs)
        car = self.get_object()
        context['ownerships'] = car.ownerships.select_related('owner').order_by('-start_date')
        return context


class CarUpdateView(UpdateView):
    """Класс-представление для обновления автомобиля"""
    model = Car
    template_name = 'car_form.html'
    fields = ['state_number', 'brand', 'model', 'color']
    success_url = reverse_lazy('cars_list_class')

    def form_valid(self, form):
        """Добавляем сообщение об успешном обновлении"""
        messages.success(self.request, f'Автомобиль {form.instance} успешно обновлен!')
        return super().form_valid(form)


class CarCreateView(CreateView):
    """Класс-представление для создания нового автомобиля"""
    model = Car
    template_name = 'car_form.html'
    fields = ['state_number', 'brand', 'model', 'color']
    success_url = reverse_lazy('cars_list_class')

    def form_valid(self, form):
        """Добавляем сообщение об успешном создании"""
        messages.success(self.request, f'Автомобиль {form.instance} успешно создан!')
        return super().form_valid(form)


from django.views.generic import DeleteView

class CarDeleteView(DeleteView):
    """Класс-представление для удаления автомобиля"""
    model = Car
    template_name = 'car_confirm_delete.html'
    success_url = reverse_lazy('cars_list_class')

    def delete(self, request, *args, **kwargs):
        """Добавляем сообщение об успешном удалении"""
        messages.success(request, f'Автомобиль успешно удален!')
        return super().delete(request, *args, **kwargs)


def home(request):
    """Главная страница"""
    # Можно добавить статистику
    owners_count = Owner.objects.count()
    cars_count = Car.objects.count()
    current_ownerships = Ownership.objects.filter(end_date__isnull=True).count()

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Система учета автовладельцев</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .container {{ max-width: 800px; margin: 0 auto; }}
            .header {{ background: #f8f9fa; padding: 20px; border-radius: 5px; }}
            .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
            .stat-item {{ text-align: center; padding: 15px; background: white; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .links {{ margin-top: 25x; }}
            .links a {{ display: inline-block; margin-right: 15px; padding: 10px 15px; 
                      background: #007bff; color: white; text-decoration: none; border-radius: 3px; }}
            .links a:hover {{ background: #0056b3; }}
            .button-row {{display: flex; justify-content: center;gap: 15px;}}
            .button-row:first-child {{margin-bottom: 12px;}}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Система учета автовладельцев</h1>
                <p>Добро пожаловать в систему управления данными об автомобилях и их владельцах</p>
            </div>

            <div class="stats">
                <div class="stat-item">
                    <h3>{owners_count}</h3>
                    <p>Владельцев</p>
                </div>
                <div class="stat-item">
                    <h3>{cars_count}</h3>
                    <p>Автомобилей</p>
                </div>
                <div class="stat-item">
                    <h3>{current_ownerships}</h3>
                    <p>Активных владений</p>
                </div>
            </div>

            <div class="links">
                <div class="button-row">
                    <a href="/admin/">Админ-панель</a>
                    <a href="/owners/">Список владельцев</a>
                    <a href="/cars/">Список автомобилей</a>
                </div>
                <div class="button-row">
                    <a href="/owner/create/" style="background: #28a745;">Добавить владельца</a>
                    <a href="/car/create/" style="background: #28a745;">Добавить автомобиль</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)