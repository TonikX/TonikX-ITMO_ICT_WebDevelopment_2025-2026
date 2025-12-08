# URL маршруты - Homework Board

## 📋 Обзор

Система маршрутизации определяет соответствие между URL адресами и представлениями Django.

## 🗺️ Структура URL

### Главный urls.py проекта

```python
# homework_board/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('assignments.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
```

### URLs приложения assignments

```python
# assignments/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Основные страницы
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    
    # Задания
    path('assignments/', views.AssignmentListView.as_view(), name='assignment_list'),
    path('assignments/<int:pk>/', views.AssignmentDetailView.as_view(), name='assignment_detail'),
    path('assignments/create/', views.AssignmentCreateView.as_view(), name='assignment_create'),
    path('assignments/<int:pk>/update/', views.AssignmentUpdateView.as_view(), name='assignment_update'),
    path('assignments/<int:pk>/delete/', views.AssignmentDeleteView.as_view(), name='assignment_delete'),
    path('assignments/<int:pk>/submit/', views.submit_assignment, name='submit_assignment'),
    
    # Оценки
    path('grades/', views.GradeListView.as_view(), name='grade_list'),
    path('grades/submission/<int:submission_id>/', views.grade_submission, name='grade_submission'),
    
    # Студенческие страницы
    path('my-submissions/', views.my_submissions, name='my_submissions'),
    path('profile/', views.profile, name='profile'),
    
    # Статистика
    path('statistics/', views.statistics, name='statistics'),
]
```

## 📍 Маршруты по категориям

### Публичные маршруты

Доступны всем пользователям (в том числе неавторизованным):

| URL | Имя | Представление | Описание |
|-----|-----|---------------|----------|
| `/` | `home` | `home` | Главная страница |
| `/register/` | `register` | `register` | Регистрация |
| `/assignments/` | `assignment_list` | `AssignmentListView` | Список заданий |
| `/assignments/<id>/` | `assignment_detail` | `AssignmentDetailView` | Детали задания |

### Маршруты для студентов

Требуют аутентификации и роли студента:

| URL | Имя | Представление | Описание |
|-----|-----|---------------|----------|
| `/assignments/<id>/submit/` | `submit_assignment` | `submit_assignment` | Сдача задания |
| `/my-submissions/` | `my_submissions` | `my_submissions` | Мои сдачи |
| `/profile/` | `profile` | `profile` | Профиль |

### Маршруты для преподавателей

Требуют роли преподавателя или администратора:

| URL | Имя | Представление | Описание |
|-----|-----|---------------|----------|
| `/assignments/create/` | `assignment_create` | `AssignmentCreateView` | Создание задания |
| `/assignments/<id>/update/` | `assignment_update` | `AssignmentUpdateView` | Редактирование |
| `/assignments/<id>/delete/` | `assignment_delete` | `AssignmentDeleteView` | Удаление |
| `/grades/submission/<id>/` | `grade_submission` | `grade_submission` | Выставление оценки |

### Маршруты оценок

| URL | Имя | Представление | Описание |
|-----|-----|---------------|----------|
| `/grades/` | `grade_list` | `GradeListView` | Список оценок |

### Статистика

| URL | Имя | Представление | Описание |
|-----|-----|---------------|----------|
| `/statistics/` | `statistics` | `statistics` | Статистика |

## 🔐 Встроенные маршруты аутентификации

Django предоставляет готовые URL для аутентификации:

```python
path('accounts/', include('django.contrib.auth.urls')),
```

**Доступные маршруты**:

| URL | Имя | Описание |
|-----|-----|----------|
| `/accounts/login/` | `login` | Вход в систему |
| `/accounts/logout/` | `logout` | Выход из системы |
| `/accounts/password_change/` | `password_change` | Смена пароля |
| `/accounts/password_change/done/` | `password_change_done` | Пароль изменен |
| `/accounts/password_reset/` | `password_reset` | Сброс пароля |
| `/accounts/password_reset/done/` | `password_reset_done` | Письмо отправлено |
| `/accounts/reset/<uidb64>/<token>/` | `password_reset_confirm` | Подтверждение |
| `/accounts/reset/done/` | `password_reset_complete` | Сброс завершен |

## 🏷️ Использование именованных URL

### В шаблонах

```html
<!-- Ссылка на список заданий -->
<a href="{% url 'assignment_list' %}">Все задания</a>

<!-- Ссылка с параметром -->
<a href="{% url 'assignment_detail' assignment.pk %}">Подробнее</a>

<!-- Редактирование -->
<a href="{% url 'assignment_update' assignment.pk %}">Редактировать</a>

<!-- С GET параметрами -->
<a href="{% url 'assignment_list' %}?subject={{ subject.id }}">Фильтр</a>
```

### В представлениях

```python
from django.urls import reverse
from django.shortcuts import redirect

# Перенаправление на список
return redirect('assignment_list')

# С параметрами
return redirect('assignment_detail', pk=assignment.pk)

# Получение URL как строки
url = reverse('assignment_detail', kwargs={'pk': 1})
```

### В формах (success_url)

```python
from django.urls import reverse_lazy

class AssignmentCreateView(CreateView):
    success_url = reverse_lazy('assignment_list')
    
    # Или динамически
    def get_success_url(self):
        return reverse_lazy('assignment_detail', kwargs={'pk': self.object.pk})
```

## 🔄 Параметры URL

### Позиционные параметры

```python
path('assignments/<int:pk>/', views.AssignmentDetailView.as_view())
```

**Типы конвертеров**:
- `<int:name>` - целое число
- `<str:name>` - строка (без `/`)
- `<slug:name>` - slug (буквы, цифры, дефис, подчеркивание)
- `<uuid:name>` - UUID
- `<path:name>` - строка с `/`

### Примеры

```python
# Детали задания по ID
path('assignments/<int:pk>/', ...)

# Фильтр по предмету (slug)
path('subject/<slug:slug>/', ...)

# Год и месяц
path('archive/<int:year>/<int:month>/', ...)
```

## 📊 Пространства имен

Для избежания конфликтов имен используйте namespace:

```python
# homework_board/urls.py
urlpatterns = [
    path('', include(('assignments.urls', 'assignments'), namespace='assignments')),
]
```

**Использование**:
```html
<a href="{% url 'assignments:assignment_list' %}">Задания</a>
```

## 🎯 Регулярные выражения (re_path)

Для сложных паттернов:

```python
from django.urls import re_path

urlpatterns = [
    re_path(r'^assignments/(?P<year>[0-9]{4})/$', views.year_archive),
    re_path(r'^assignments/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive),
]
```

## 🔍 GET параметры

### В URL

```
/assignments/?search=математика&subject=1&status=active
```

### В представлении

```python
def assignment_list(request):
    search = request.GET.get('search', '')
    subject_id = request.GET.get('subject')
    status = request.GET.get('status')
```

### В шаблоне

```html
<a href="{% url 'assignment_list' %}?status=active">Активные</a>

<!-- Сохранение существующих параметров -->
<a href="?{{ request.GET.urlencode }}&page=2">Страница 2</a>
```

## 🛡️ Защита маршрутов

### Декоратор login_required

```python
from django.contrib.auth.decorators import login_required

@login_required
def my_submissions(request):
    # ...
```

**Настройки**:
```python
# settings.py
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
```

### Классовые представления

```python
from django.contrib.auth.mixins import LoginRequiredMixin

class MySubmissionsView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
```

## 🗺️ Карта сайта

Полная структура URL приложения:

```
/                                   # Главная
├── register/                       # Регистрация
├── assignments/                    # Список заданий
│   ├── <id>/                      # Детали задания
│   ├── <id>/submit/               # Сдача задания
│   ├── <id>/update/               # Редактирование
│   ├── <id>/delete/               # Удаление
│   └── create/                    # Создание
├── grades/                        # Оценки
│   └── submission/<id>/          # Выставление оценки
├── my-submissions/                # Мои сдачи
├── profile/                       # Профиль
├── statistics/                    # Статистика
└── accounts/                      # Аутентификация
    ├── login/
    ├── logout/
    ├── password_change/
    └── password_reset/
```

## 🧪 Тестирование URL

```python
from django.test import TestCase
from django.urls import reverse

class URLTests(TestCase):
    def test_home_url(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
    
    def test_assignment_detail_url(self):
        # Создаем задание
        assignment = Assignment.objects.create(...)
        url = reverse('assignment_detail', args=[assignment.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
```

---

!!! info "Документация Django"
    Подробнее о URL dispatcher: [Django URL dispatcher](https://docs.djangoproject.com/en/stable/topics/http/urls/)
