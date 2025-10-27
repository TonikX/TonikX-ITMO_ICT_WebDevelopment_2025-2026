# Архитектура проекта

## Структура проекта
```
hotel_booking/
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3
├── hotel_booking/          # Основной пакет проекта
│   ├── __init__.py
│   ├── settings.py         # Настройки Django
│   ├── urls.py             # Корневые URL
│   ├── wsgi.py
│   └── asgi.py
├── booking/                # Приложение бронирования
│   ├── __init__.py
│   ├── models.py           # Модели данных
│   ├── views.py            # Представления (контроллеры)
│   ├── forms.py            # Формы
│   ├── services.py         # Бизнес-логика
│   ├── admin.py            # Административная панель
│   ├── urls.py             # URL приложения
│   ├── tests.py            # Тесты
│   └── management/
│       └── commands/
│           └── seed_demo_data.py  # Команда для генерации тестовых данных
│
└── templates/              # HTML шаблоны
    ├── base.html
    ├── registration/
    │   ├── login.html
    │   ├── register.html
    │   └── password_reset_form.html
    └── booking/
        ├── hotel_list.html
        ├── hotel_detail.html
        ├── room_list.html
        ├── booking_*.html
        └── review_*.html
```

## Архитектурные решения

### MVC (MTV в Django)

Проект следует архитектуре MTV (Model-Template-View), характерной для Django:

- **Models** (`models.py`): Определение структуры данных и бизнес-логики на уровне моделей
- **Templates** (`templates/`): Представление данных пользователю
- **Views** (`views.py`): Обработка запросов и связь между моделями и шаблонами

### Слой сервисов

Для отделения бизнес-логики от представлений используется отдельный модуль `services.py`:
```python
# Примеры функций в services.py
- check_room_availability()     # Проверка доступности номера
- get_available_rooms()          # Получение доступных номеров
- calculate_booking_price()      # Расчёт стоимости бронирования
- can_check_in() / can_check_out()  # Валидация переходов статусов
- get_recent_guests()            # Получение постояльцев за период
```

### Формы и валидация

Все формы наследуются от `forms.ModelForm` и содержат:

- Валидацию на уровне полей (`clean_<field>`)
- Комплексную валидацию (`clean()`)
- Кастомную логику сохранения (`save()`)

### Права доступа

Используются встроенные миксины Django:

- `LoginRequiredMixin` - для представлений, требующих авторизации
- Проверка владельца через `get_queryset()` - фильтрация по `user=request.user`
- Проверка прав на редактирование через свойства модели (`can_edit`, `can_cancel`)

## Паттерны проектирования

### 1. Repository Pattern (частично)

Сложные запросы к БД инкапсулированы в функции `services.py`:
```python
def get_available_rooms(check_in, check_out, hotel=None):
    # Логика получения доступных номеров
    pass
```

### 2. Factory Pattern

Использование Django Class-Based Views как фабрик представлений:
```python
class BookingCreateView(LoginRequiredMixin, CreateView):
    # Стандартное создание с кастомизацией через методы
    pass
```

### 3. Template Method Pattern

CBV используют шаблонный метод с переопределением хуков:

- `get_queryset()` - получение набора данных
- `get_context_data()` - дополнение контекста
- `form_valid()` - обработка валидной формы
- `get_form_kwargs()` - настройка параметров формы

## Безопасность

### CSRF Protection
Все формы защищены токенами CSRF через `{% csrf_token %}`

### SQL Injection Protection
Использование ORM Django предотвращает SQL-инъекции

### XSS Protection
Автоматическое экранирование в Django Templates

### Аутентификация
- Хеширование паролей через встроенные механизмы Django
- Сессии для хранения состояния аутентификации

## Масштабируемость

### Пагинация
Используется встроенная пагинация Django для больших списков (10-20 элементов на страницу)

### Оптимизация запросов
- `select_related()` для FK (уменьшение числа запросов)
- `prefetch_related()` для M2M (оптимизация связанных данных)
- Индексы на часто используемые поля (`db_index=True`)
