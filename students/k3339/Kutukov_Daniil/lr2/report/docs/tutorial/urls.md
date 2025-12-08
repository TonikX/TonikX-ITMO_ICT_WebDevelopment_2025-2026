# URL маршруты - Tutorial

## 📋 Обзор

Система маршрутизации определяет соответствие между URL и представлениями.

## 🗺️ Структура URL

### Главный urls.py

```python
# django_project_tonikx/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('project_first_app.urls')),
]
```

### URLs приложения

```python
# project_first_app/urls.py
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # Маршруты для аутентификации
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Маршруты для владельцев (функциональные представления)
    path('owners/', views.owners_list, name='owners_list'),
    path('owner/<int:owner_id>/', views.owner_detail, name='owner_detail'),
    path('owner/create/', views.owner_create, name='owner_create'),
    path('owner/<int:owner_id>/update/', views.owner_update, name='owner_update'),
    path('owner/<int:owner_id>/delete/', views.owner_delete, name='owner_delete'),
    
    # Маршруты для автомобилей (классовые представления)
    path('cars/', views.CarListView.as_view(), name='car_list'), 
    path('cars/<int:pk>/', views.CarDetailView.as_view(), name='car_detail'),
    path('cars/create/', views.CarCreateView.as_view(), name='car_create'),
    path('cars/<int:pk>/update/', views.CarUpdateView.as_view(), name='car_update'),
    path('cars/<int:pk>/delete/', views.CarDeleteView.as_view(), name='car_delete'),
]
```

## 📍 Таблица маршрутов

### Общие

| URL | Имя | Представление | Тип | Описание |
|-----|-----|---------------|------|----------|
| `/` | `home` | `home` | FBV | Главная страница |

### Аутентификация

| URL | Имя | Представление | Тип | Описание |
|-----|-----|---------------|------|----------|
| `/register/` | `register` | `register` | FBV | Регистрация |
| `/profile/` | `profile` | `profile` | FBV | Профиль |
| `/accounts/login/` | `login` | Django | - | Вход |
| `/accounts/logout/` | `logout` | Django | - | Выход |

### Владельцы (FBV)

| URL | Имя | Представление | Тип | Описание |
|-----|-----|---------------|------|----------|
| `/owners/` | `owners_list` | `owners_list` | FBV | Список владельцев |
| `/owner/<id>/` | `owner_detail` | `owner_detail` | FBV | Детали владельца |
| `/owner/create/` | `owner_create` | `owner_create` | FBV | Создание владельца |
| `/owner/<id>/update/` | `owner_update` | `owner_update` | FBV | Редактирование |
| `/owner/<id>/delete/` | `owner_delete` | `owner_delete` | FBV | Удаление |

### Автомобили (CBV)

| URL | Имя | Представление | Тип | Описание |
|-----|-----|---------------|------|----------|
| `/cars/` | `car_list` | `CarListView` | ListView | Список автомобилей |
| `/cars/<pk>/` | `car_detail` | `CarDetailView` | DetailView | Детали автомобиля |
| `/cars/create/` | `car_create` | `CarCreateView` | CreateView | Создание автомобиля |
| `/cars/<pk>/update/` | `car_update` | `CarUpdateView` | UpdateView | Редактирование |
| `/cars/<pk>/delete/` | `car_delete` | `CarDeleteView` | DeleteView | Удаление |

## 🏷️ Использование именованных URL

### В шаблонах

```html
<!-- Список владельцев -->
<a href="{% url 'owners_list' %}">Все владельцы</a>

<!-- Детали с параметром -->
<a href="{% url 'owner_detail' owner.id %}">Подробнее</a>

<!-- Редактирование -->
<a href="{% url 'owner_update' owner.id %}">Редактировать</a>

<!-- Список автомобилей -->
<a href="{% url 'car_list' %}">Все автомобили</a>

<!-- Детали автомобиля -->
<a href="{% url 'car_detail' car.pk %}">{{ car }}</a>
```

### В представлениях

```python
from django.urls import reverse
from django.shortcuts import redirect

# Функциональные представления
return redirect('owners_list')
return redirect('owner_detail', owner_id=owner.id)

# Классовые представления
def get_success_url(self):
    return reverse('car_detail', kwargs={'pk': self.object.pk})
```

## 🔤 Параметры URL

### Для функциональных представлений

```python
path('owner/<int:owner_id>/', views.owner_detail, name='owner_detail')
```

В представлении:
```python
def owner_detail(request, owner_id):
    owner = User.objects.get(pk=owner_id)
    # ...
```

### Для классовых представлений

```python
path('cars/<int:pk>/', views.CarDetailView.as_view(), name='car_detail')
```

CBV автоматически использует параметр `pk`.

## 🎯 Встроенные маршруты аутентификации

```python
path('accounts/', include('django.contrib.auth.urls'))
```

Предоставляет:

| URL | Имя | Описание |
|-----|-----|----------|
| `/accounts/login/` | `login` | Вход |
| `/accounts/logout/` | `logout` | Выход |
| `/accounts/password_change/` | `password_change` | Смена пароля |
| `/accounts/password_reset/` | `password_reset` | Сброс пароля |

## 🗺️ Карта сайта

```
/                              # Главная страница
├── register/                  # Регистрация
├── profile/                   # Профиль
├── accounts/                  # Аутентификация
│   ├── login/
│   └── logout/
├── owners/                    # Владельцы (FBV)
│   ├── <id>/                 # Детали
│   ├── <id>/update/          # Редактирование
│   ├── <id>/delete/          # Удаление
│   └── create/               # Создание
└── cars/                      # Автомобили (CBV)
    ├── <pk>/                 # Детали
    ├── <pk>/update/          # Редактирование
    ├── <pk>/delete/          # Удаление
    └── create/               # Создание
```

## 🔍 Различия в параметрах

### FBV - используют именованные параметры

```python
path('owner/<int:owner_id>/', ...)

def owner_detail(request, owner_id):
    # используется owner_id
```

### CBV - используют pk

```python
path('cars/<int:pk>/', ...)

class CarDetailView(DetailView):
    # автоматически использует pk
```

## ✅ Примеры использования

### Навигация между разными моделями

```html
<!-- В шаблоне владельца -->
{% for ownership in ownerships %}
    <a href="{% url 'car_detail' ownership.car.pk %}">
        {{ ownership.car }}
    </a>
{% endfor %}

<!-- В шаблоне автомобиля -->
{% for ownership in ownerships %}
    <a href="{% url 'owner_detail' ownership.owner.id %}">
        {{ ownership.owner }}
    </a>
{% endfor %}
```

### Перенаправления после действий

```python
# После создания владельца
return redirect('owner_detail', owner_id=owner.id)

# После удаления
return redirect('owners_list')

# В CBV
class CarCreateView(CreateView):
    success_url = '/cars/'  # или
    
    def get_success_url(self):
        return reverse('car_list')
```

---

!!! info "Документация"
    Подробнее: [Django URL dispatcher](https://docs.djangoproject.com/en/stable/topics/http/urls/)
