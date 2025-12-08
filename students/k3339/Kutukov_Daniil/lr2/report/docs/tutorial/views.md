# Представления - Tutorial

## 📋 Обзор

Проект демонстрирует два подхода к созданию представлений в Django:

- **Функциональные представления** (FBV) - для управления владельцами
- **Классовые представления** (CBV) - для управления автомобилями

## 🏠 Главная страница

### `home(request)`

```python
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
```

**URL**: `/`  
**Template**: `home.html`  
**Контекст**: статистика и список последних владельцев

## 👥 Функциональные представления (Владельцы)

### `owners_list(request)`

Список всех владельцев.

```python
def owners_list(request):
    """Функциональное представление для вывода всех владельцев"""
    context = {}
    context["dataset"] = User.objects.all()
    return render(request, "owners_list.html", context)
```

**URL**: `/owners/`  
**Template**: `owners_list.html`

### `owner_detail(request, owner_id)`

Детальная информация о владельце.

```python
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
```

**URL**: `/owner/<int:owner_id>/`  
**Template**: `owner.html`  
**Особенности**:
- Использует `select_related()` для оптимизации
- Обработка несуществующего владельца через Http404

### `owner_create(request)`

Создание нового владельца.

```python
@login_required
def owner_create(request):
    """Создание нового владельца"""
    if request.method == 'POST':
        form = OwnerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Владелец успешно создан!')
            return redirect('owners_list')
    else:
        form = OwnerForm()
    
    return render(request, 'owner_form.html', {
        'form': form,
        'action': 'create'
    })
```

**URL**: `/owner/create/`  
**Требует аутентификации**: Да

### `owner_update(request, owner_id)`

Редактирование владельца.

```python
@login_required
def owner_update(request, owner_id):
    """Редактирование владельца"""
    owner = get_object_or_404(User, pk=owner_id)
    
    if request.method == 'POST':
        form = OwnerForm(request.POST, instance=owner)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные обновлены!')
            return redirect('owner_detail', owner_id=owner.id)
    else:
        form = OwnerForm(instance=owner)
    
    return render(request, 'owner_form.html', {
        'form': form,
        'action': 'update',
        'owner': owner
    })
```

**URL**: `/owner/<int:owner_id>/update/`

### `owner_delete(request, owner_id)`

Удаление владельца.

```python
@login_required
def owner_delete(request, owner_id):
    """Удаление владельца"""
    owner = get_object_or_404(User, pk=owner_id)
    
    if request.method == 'POST':
        owner.delete()
        messages.success(request, 'Владелец удален!')
        return redirect('owners_list')
    
    return render(request, 'owner_confirm_delete.html', {'owner': owner})
```

**URL**: `/owner/<int:owner_id>/delete/`

## 🚗 Классовые представления (Автомобили)

### CarListView

```python
class CarListView(ListView):
    """Классовое представление для вывода списка автомобилей"""
    model = Car
    template_name = 'car_list.html'
    context_object_name = 'cars'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список автомобилей'
        return context
```

**URL**: `/cars/`  
**Template**: `car_list.html`  
**Базовый класс**: `ListView`

### CarDetailView

```python
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
```

**URL**: `/cars/<int:pk>/`  
**Template**: `car_detail.html`

### CarCreateView

```python
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
```

**URL**: `/cars/create/`  
**Template**: `car_form.html`

### CarUpdateView

```python
class CarUpdateView(UpdateView):
    """Классовое представление для обновления автомобиля"""
    model = Car
    fields = ['brand', 'model', 'color', 'state_number']
    template_name = 'car_form.html'
    
    def get_success_url(self):
        return f'/cars/{self.object.pk}/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать автомобиль'
        context['action'] = 'update'
        return context
```

**URL**: `/cars/<int:pk>/update/`

### CarDeleteView

```python
class CarDeleteView(DeleteView):
    """Классовое представление для удаления автомобиля"""
    model = Car
    template_name = 'car_confirm_delete.html'
    success_url = '/cars/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удалить автомобиль'
        return context
```

**URL**: `/cars/<int:pk>/delete/`  
**Template**: `car_confirm_delete.html`

## 🔐 Аутентификация

### `register(request)`

```python
def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})
```

**URL**: `/register/`

### `profile(request)`

```python
@login_required
def profile(request):
    """Профиль пользователя"""
    ownerships = Ownership.objects.filter(
        owner=request.user
    ).select_related('car')
    
    licenses = DriverLicense.objects.filter(owner=request.user)
    
    context = {
        'ownerships': ownerships,
        'licenses': licenses,
    }
    return render(request, 'profile.html', context)
```

**URL**: `/profile/`  
**Требует аутентификации**: Да

## 📊 Сравнение подходов

### Функциональные представления (FBV)

**Преимущества**:
- Простота и понятность
- Прямой контроль над логикой
- Легко настраивать

**Недостатки**:
- Больше кода для CRUD
- Повторение логики

### Классовые представления (CBV)

**Преимущества**:
- Меньше кода
- Переиспользование через наследование
- DRY (Don't Repeat Yourself)

**Недостатки**:
- Сложнее для начинающих
- Скрытая логика

## 🔍 Оптимизация запросов

```python
# Плохо - N+1 запросов
ownerships = Ownership.objects.filter(owner=owner)
for o in ownerships:
    print(o.car.brand)  # Отдельный запрос для каждого car!

# Хорошо - 1 запрос
ownerships = Ownership.objects.filter(owner=owner).select_related('car')
for o in ownerships:
    print(o.car.brand)  # Данные уже загружены
```

---

!!! info "Выбор подхода"
    Используйте CBV для стандартных CRUD операций и FBV для сложной бизнес-логики.
