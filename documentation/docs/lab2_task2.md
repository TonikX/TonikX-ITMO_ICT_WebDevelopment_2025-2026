# Практическая работа №2 — Реализация CRUD в Django

**Автор:** Ермаков Максим  
**Группа:** К3340  

---

## Цель работы
Освоить принципы реализации CRUD-интерфейсов (Create, Read, Update, Delete) средствами Django, используя функциональные и классовые представления, формы и шаблоны.

---

## Задача 1 — Доработка модели данных (связь «многие ко многим»)

### Цель
Правильно реализовать связь между владельцем, автомобилем и владением, используя механизм ManyToMany.

### Ход выполнения

В модели `Owner` добавлено поле `cars`, использующее ассоциативную сущность `Ownership` для связи с автомобилями.

```python
from django.db import models

class Owner(models.Model):
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    birth_date = models.DateField(null=True, blank=True)
    cars = models.ManyToManyField('Car', through='Ownership', related_name='owners')

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Car(models.Model):
    plate_number = models.CharField(max_length=15, unique=True)
    make = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    color = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.plate_number})"


class Ownership(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='ownerships')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='ownerships')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = [('owner', 'car', 'start_date')]
```

### Результат
Связь между владельцем и автомобилем реализована корректно через модель `Ownership`, что обеспечивает возможность хранить периоды владения и исключать пересечения по датам.

---

## Задача 2 — Работа с представлениями (контроллерами)

### Цель
Научиться использовать два подхода к построению представлений (views):  
- **функциональные** (Function-Based Views, FBV),  
- **классовые** (Class-Based Views, CBV).

---

### 2.1 Представления на функциях

Пример FBV для вывода всех владельцев:

```python
from django.shortcuts import render
from .models import Owner

def owners_list(request):
    owners = Owner.objects.all()
    return render(request, "owners_list.html", {"owners": owners})
```

Шаблон `owners_list.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Owners list</title></head>
<body>
<h1>Список владельцев</h1>
<ul>
{% for owner in owners %}
  <li>{{ owner.last_name }} {{ owner.first_name }} — {{ owner.birth_date }}</li>
{% endfor %}
</ul>
</body>
</html>
```

Адресация (`urls.py`):
```python
from django.urls import path
from .views import owners_list

urlpatterns = [
    path('owners/', owners_list, name='owners_list'),
]
```

---

### 2.2 Представления на классах

#### Список автомобилей
```python
from django.views.generic import ListView
from .models import Car

class CarListView(ListView):
    model = Car
    template_name = 'car_list.html'
    ordering = ['make']
```
Шаблон `car_list.html`:
```html
<h1>Список автомобилей</h1>
<ul>
{% for car in object_list %}
  <li><a href="/cars/{{ car.pk }}/">{{ car.make }} {{ car.model }}</a></li>
{% empty %}
  <li>Нет автомобилей</li>
{% endfor %}
</ul>
```

#### Детальная информация о машине
```python
from django.views.generic import DetailView

class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'
```

Шаблон `car_detail.html`:
```html
<h1>{{ object.make }} {{ object.model }}</h1>
<p>Номер: {{ object.plate_number }}</p>
<p>Цвет: {{ object.color }}</p>
<a href="/cars/{{ object.pk }}/update/">Редактировать</a>
```

#### Обновление автомобиля
```python
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

class CarUpdateView(UpdateView):
    model = Car
    fields = ['plate_number', 'make', 'model', 'color']
    template_name = 'car_form.html'
    success_url = reverse_lazy('car_list')
```

#### Удаление автомобиля
```python
from django.views.generic.edit import DeleteView

class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_confirm_delete.html'
    success_url = reverse_lazy('car_list')
```

Адресация:
```python
path('cars/', CarListView.as_view(), name='car_list'),
path('cars/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
path('cars/<int:pk>/update/', CarUpdateView.as_view(), name='car_update'),
path('cars/<int:pk>/delete/', CarDeleteView.as_view(), name='car_delete'),
```

### Результат
Созданы FBV и CBV-представления, позволяющие просматривать владельцев и автомобили, а также редактировать и удалять записи.

---

## Задача 3 — Работа с формами и представлениями

### Цель
Освоить работу с Django-формами, реализовать ввод и редактирование данных через веб-интерфейс.

---

### 3.1 Формы на основе функций (FBV)

**Форма для создания владельца:**

`forms.py`:
```python
from django import forms
from .models import Owner

class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['last_name', 'first_name', 'birth_date']
```

**Контроллер:**
```python
from django.shortcuts import render
from .forms import OwnerForm

def owner_create(request):
    form = OwnerForm(request.POST or None)
    if form.is_valid():
        form.save()
    return render(request, "owner_create.html", {"form": form})
```

**Шаблон `owner_create.html`:**
```html
<h1>Добавить владельца</h1>
<form method="post">{% csrf_token %}
  {{ form.as_p }}
  <input type="submit" value="Сохранить">
</form>
```

**URL:**
```python
path('owners/create/', owner_create, name='owner_create'),
```

---

### 3.2 Формы на основе классов (CBV)

#### Создание автомобиля
```python
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Car

class CarCreateView(CreateView):
    model = Car
    fields = ['plate_number', 'make', 'model', 'color']
    template_name = 'car_form.html'
    success_url = reverse_lazy('car_list')
```

#### Удаление автомобиля
```python
class CarDeleteView(DeleteView):
    model = Car
    template_name = 'car_confirm_delete.html'
    success_url = reverse_lazy('car_list')
```

Шаблоны для Create/Update одинаковые (`car_form.html`):
```html
<h1>Редактирование автомобиля</h1>
<form method="post">{% csrf_token %}
  {{ form.as_p }}
  <input type="submit" value="Сохранить">
</form>
```

Удаление (`car_confirm_delete.html`):
```html
<h1>Удалить автомобиль</h1>
<p>Вы уверены, что хотите удалить {{ object }}?</p>
<form method="post">{% csrf_token %}
  <input type="submit" value="Удалить">
</form>
```

---

### Результат

✅ Реализованы формы для создания владельцев (FBV) и автомобилей (CBV).  
✅ Настроены шаблоны и маршруты.  
✅ Проверено добавление, обновление и удаление записей в базе.

---

## Вывод

В ходе практической работы №2 были реализованы все основные CRUD-операции в Django:  
- просмотр списков и деталей объектов;  
- добавление и редактирование данных через формы;  
- удаление записей из базы данных.  
Освоены оба подхода к построению представлений — функциональный (FBV) и классовый (CBV).
