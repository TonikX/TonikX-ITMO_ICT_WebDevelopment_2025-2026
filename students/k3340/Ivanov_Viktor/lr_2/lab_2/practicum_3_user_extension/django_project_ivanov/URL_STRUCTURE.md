# Структура URL-адресов проекта

## Главный файл URLs (django_project_ivanov/urls.py)

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),              # Админ-панель
    path('', include('project_first_app.urls')),  # Подключение URLs приложения
]
```

## URLs приложения (project_first_app/urls.py)

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.owner_list, name='owner_list'),
    path('owner/<int:owner_id>/', views.owner_detail, name='owner_detail'),
]
```

## Доступные URL-адреса

### 1. Главная страница - Список владельцев
**URL:** `http://127.0.0.1:8000/`  
**Контроллер:** `views.owner_list`  
**Шаблон:** `templates/owner_list.html`  
**Описание:** Отображает список всех владельцев автомобилей

**Пример использования:**
```bash
curl http://127.0.0.1:8000/
```

---

### 2. Информация о владельце
**URL:** `http://127.0.0.1:8000/owner/<int:owner_id>/`  
**Контроллер:** `views.owner_detail`  
**Шаблон:** `templates/owner.html`  
**Параметр:** `owner_id` - целое число (ID владельца)  
**Описание:** Отображает подробную информацию о конкретном владельце

**Примеры использования:**
```bash
# Просмотр владельца с ID=1
curl http://127.0.0.1:8000/owner/1/

# Просмотр владельца с ID=2
curl http://127.0.0.1:8000/owner/2/
```

**Обработка ошибок:**
- Если владелец не найден, возвращается HTTP 404
- Отображается сообщение: "Владелец не найден"

---

### 3. Админ-панель
**URL:** `http://127.0.0.1:8000/admin/`  
**Встроенный Django Admin**  
**Описание:** Административная панель для управления данными

**Учетные данные:**
- Логин: `admin`
- Пароль: `admin`

---

## Схема маршрутизации

```
http://127.0.0.1:8000/
│
├── /                              → owner_list (главная страница)
│   └── Показывает всех владельцев
│
├── /owner/1/                      → owner_detail (владелец #1)
├── /owner/2/                      → owner_detail (владелец #2)
├── /owner/<int:owner_id>/         → owner_detail (любой владелец)
│   └── Показывает информацию о конкретном владельце
│
└── /admin/                        → Django Admin
    ├── /admin/login/
    └── /admin/project_first_app/
        ├── avtovladelec/
        ├── avtomobil/
        ├── vladenie/
        └── voditelskoe_udostoverenie/
```

---

## Передача параметров в URL

### Синтаксис

```python
path('owner/<int:owner_id>/', views.owner_detail, name='owner_detail')
```

**Компоненты:**
- `owner/` - фиксированная часть URL
- `<int:owner_id>` - динамический параметр:
  - `int` - конвертер типа (только целые числа)
  - `owner_id` - имя параметра, передаваемое в функцию представления

### Контроллер получает параметр

```python
def owner_detail(request, owner_id):
    # owner_id автоматически передается из URL
    owner = Avtovladelec.objects.get(pk=owner_id)
    ...
```

---

## Доступные конвертеры типов Django

| Конвертер | Описание | Пример URL |
|-----------|----------|------------|
| `str` | Любая строка (не пустая, без `/`) | `<str:username>` |
| `int` | Целое положительное число | `<int:owner_id>` |
| `slug` | Строка с буквами, цифрами, дефисом, подчеркиванием | `<slug:article_slug>` |
| `uuid` | UUID строка | `<uuid:object_id>` |
| `path` | Любая строка (включая `/`) | `<path:file_path>` |

---

## Использование в шаблонах

### Создание ссылок с параметрами

```django
{# Ссылка на владельца с ID=1 #}
<a href="{% url 'owner_detail' 1 %}">Владелец 1</a>

{# Ссылка с переменной #}
<a href="{% url 'owner_detail' owner.id_vladelca %}">
    {{ owner.familiya }} {{ owner.imya }}
</a>

{# Ссылка на главную #}
<a href="{% url 'owner_list' %}">Вернуться к списку</a>
```

---

## Тестирование URL-адресов

### Успешный запрос (200 OK)
```bash
curl -I http://127.0.0.1:8000/owner/1/
# HTTP/1.1 200 OK
```

### Несуществующий владелец (404 Not Found)
```bash
curl -I http://127.0.0.1:8000/owner/999/
# HTTP/1.1 404 Not Found
```

### Неверный формат параметра (404)
```bash
curl -I http://127.0.0.1:8000/owner/abc/
# HTTP/1.1 404 Not Found
# (abc не является целым числом)
```

---

## Именование URL-маршрутов

Каждый маршрут имеет уникальное имя для использования в коде:

```python
urlpatterns = [
    path('', views.owner_list, name='owner_list'),           # имя: owner_list
    path('owner/<int:owner_id>/', views.owner_detail, name='owner_detail'),  # имя: owner_detail
]
```

**Преимущества:**
- Можно изменить URL без изменения кода в шаблонах
- Централизованное управление маршрутизацией
- Более читаемый код

---

## Результат выполнения задания 5

✅ Создан файл `urls.py` в приложении `project_first_app`  
✅ Файл импортирован в главный `urls.py` проекта  
✅ Настроен URL-адрес с передачей параметра `owner_id`  
✅ По адресу `http://127.0.0.1:8000/owner/1/` доступна страница первого владельца  
✅ По адресу `http://127.0.0.1:8000/owner/2/` доступна страница второго владельца  
✅ Реализована обработка ошибки 404 для несуществующих владельцев  

---

## Дополнительная информация

**Официальная документация Django:**
- URL диспетчеризация: https://docs.djangoproject.com/en/5.2/topics/http/urls/
- Конвертеры путей: https://docs.djangoproject.com/en/5.2/topics/http/urls/#path-converters
- URL в шаблонах: https://docs.djangoproject.com/en/5.2/ref/templates/builtins/#url

