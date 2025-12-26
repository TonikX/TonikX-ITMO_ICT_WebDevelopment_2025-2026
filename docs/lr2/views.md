# Представления и шаблоны

## Введение

Представления (views) - это код, который обрабатывает запросы пользователей и возвращает ответы. Шаблоны (templates) - это HTML файлы, которые определяют, как будет выглядеть страница.

## Типы представлений

В проекте я использовала два подхода:

### Class-Based Views (CBV)

Это готовые классы Django для стандартных операций. Они экономят время и код.

**Преимущества:**

- Меньше кода
- Встроенная функциональность
- Легко расширять через миксины

**Недостатки:**

- Сложнее понять, как работает
- Меньше гибкости

### Function-Based Views (FBV)

Это обычные функции Python. Их я использовала для специфичной логики.

**Преимущества:**

- Проще понять
- Полный контроль над логикой

**Недостатки:**

- Больше кода
- Нужно больше всего делать вручную

## Основные представления

### Список гонок (RaceListView)

**Тип:** ListView (CBV)

**URL:** `/` (главная страница)

**Функции:**

- Показывает список опубликованных гонок
- Поиск по названию, месту, описанию
- Сортировка
- Пагинация (6 гонок на страницу)

**Код:**

```python
class RaceListView(ListView):
    model = Race
    template_name = 'racing/race_list.html'
    context_object_name = 'races'
    paginate_by = 6
    
    def get_queryset(self):
        queryset = Race.objects.filter(is_published=True)
        
        # Поиск
        search_query = self.request.GET.get('search', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(location__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        # Сортировка
        sort_by = self.request.GET.get('sort', '-date')
        if sort_by in ['date', '-date', 'title', '-title', 'location', '-location']:
            queryset = queryset.order_by(sort_by)
        
        return queryset
```

### Детальная информация о гонке (RaceDetailView)

**Тип:** DetailView (CBV)

**URL:** `/race/<id>/`

**Функции:**

- Показывает информацию о гонке
- Список заездов и результатов
- Список зарегистрированных участников (с поиском и пагинацией)
- Форму для регистрации
- Форму для комментариев
- Список комментариев

**Особенности:**

В `get_context_data` я добавляю много дополнительных данных:

```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    race = self.object
    
    # Заезды с результатами
    heats_with_results = []
    for heat in race.heats.all():
        results = heat.results.order_by('position')
        heats_with_results.append({'heat': heat, 'results': results})
    
    context['heats_with_results'] = heats_with_results
    
    # Участники с пагинацией
    registrations = race.registrations.filter(active=True)
    # ... поиск и сортировка ...
    paginator = Paginator(registrations, 6)
    context['registrations'] = paginator.get_page(page_number)
    
    # Формы и комментарии
    context['comments'] = race.comments.all()
    context['registration_form'] = RegistrationForm()
    context['comment_form'] = CommentForm()
    
    return context
```

### Регистрация на гонку (register_for_race)

**Тип:** Function-Based View

**URL:** `/race/<id>/register/`

**Метод:** POST

**Логика:**

```python
@login_required
def register_for_race(request, pk):
    race = get_object_or_404(Race, pk=pk)
    
    # Проверка профиля
    try:
        driver_profile = request.user.driver_profile
        if not driver_profile.full_name or driver_profile.full_name.strip() == '':
            messages.warning(request, 'Заполните профиль')
            return redirect('driverprofile_update')
    except DriverProfile.DoesNotExist:
        messages.error(request, 'Сначала заполните профиль')
        return redirect('driverprofile_update')
    
    # Проверка существующей регистрации
    existing = Registration.objects.filter(
        driver=driver_profile, race=race, active=True
    ).first()
    
    if existing:
        messages.warning(request, 'Вы уже зарегистрированы')
        return redirect('race_detail', pk=pk)
    
    # Создание регистрации
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.driver = driver_profile
            registration.race = race
            registration.save()
            messages.success(request, 'Регистрация успешна')
        return redirect('race_detail', pk=pk)
```

Я выбрала FBV для этой функции, потому что логика специфичная и не подходит под стандартные CBV.

### Мои регистрации (RegistrationListView)

**Тип:** ListView (CBV)

**URL:** `/registrations/`

**Функции:**

- Для обычных пользователей - только их регистрации
- Для админов - все регистрации
- Поиск и сортировка
- Пагинация (15 на страницу)

**Код:**

```python
class RegistrationListView(LoginRequiredMixin, ListView):
    model = Registration
    template_name = 'racing/registration_list.html'
    paginate_by = 15
    
    def get_queryset(self):
        is_admin = self.request.user.is_staff or self.request.user.is_superuser
        
        if is_admin:
            queryset = Registration.objects.filter(active=True)
        else:
            queryset = Registration.objects.filter(
                driver=self.request.user.driver_profile,
                active=True
            )
        
        # Поиск и сортировка...
        return queryset
```

### Редактирование и удаление

Для редактирования и удаления объектов используются:

- **UpdateView** - редактирование
- **DeleteView** - удаление

С добавлением миксинов:

- **LoginRequiredMixin** - только для авторизованных
- **OwnerRequiredMixin** - только владелец или админ

**Пример:**

```python
class RegistrationUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Registration
    form_class = RegistrationForm
    template_name = 'racing/registration_form.html'
    success_url = reverse_lazy('registration_list')
```

## Шаблоны

### Базовый шаблон (base.html)

Содержит общие элементы всех страниц:

- HTML структуру
- Подключение Bootstrap 5
- Навигационное меню
- Блок для сообщений
- Футер

**Основные блоки:**

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Табло победителей{% endblock %}</title>
    <!-- Bootstrap CSS -->
</head>
<body>
    <nav class="navbar">
        <!-- Меню навигации -->
    </nav>
    
    <div class="container">
        <!-- Сообщения -->
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }}">
                    {{ message }}
                </div>
            {% endfor %}
        {% endif %}
        
        <!-- Основной контент -->
        {% block content %}
        {% endblock %}
    </div>
    
    <footer>
        <!-- Футер -->
    </footer>
</body>
</html>
```

### Меню навигации

Меню адаптируется в зависимости от статуса пользователя:

**Для неавторизованных:**

- Гонки
- Войти
- Регистрация

**Для обычных пользователей:**

- Гонки
- Мои регистрации
- Профиль
- Сменить пароль
- Выйти

**Для администраторов:**

- Гонки
- Все регистрации
- Профиль
- Admin Panel (красная метка)
- Сменить пароль
- Выйти (с короной)

**Код:**

```html
{% if user.is_authenticated %}
    <li class="nav-item">
        <a class="nav-link" href="{% url 'registration_list' %}">
            {% if user.is_staff or user.is_superuser %}
                Все регистрации
            {% else %}
                Мои регистрации
            {% endif %}
        </a>
    </li>
    
    {% if user.is_staff or user.is_superuser %}
        <li class="nav-item">
            <a class="nav-link" href="{% url 'admin:index' %}">
                <span class="badge bg-danger">Admin Panel</span>
            </a>
        </li>
    {% endif %}
{% endif %}
```

### Список гонок (race_list.html)

**Структура:**

1. Заголовок
2. Форма поиска и сортировки
3. Сетка карточек с гонками
4. Пагинация

**Карточка гонки:**

```html
<div class="card race-card h-100">
    <div class="card-body">
        <h5 class="card-title">{{ race.title }}</h5>
        <h6 class="card-subtitle mb-2 text-muted">{{ race.location }}</h6>
        <p class="card-text">Дата: {{ race.date|date:"d.m.Y" }}</p>
        <p class="card-text">{{ race.description|truncatechars:100 }}</p>
    </div>
    <div class="card-footer text-end">
        <a href="{% url 'race_detail' race.pk %}" class="btn btn-primary">Подробнее</a>
    </div>
</div>
```

### Страница гонки (race_detail.html)

Самый сложный шаблон, содержит:

1. Информацию о гонке
2. Список заездов с результатами
3. Форму поиска участников
4. Список участников с пагинацией
5. Форму регистрации (если не зарегистрирован)
6. Форму для комментариев
7. Список комментариев

**Таблица результатов заезда:**

```html
<table class="table table-hover">
    <thead>
        <tr>
            <th>#</th>
            <th>Водитель</th>
            <th>Команда</th>
            <th>Класс</th>
            <th>Время</th>
            <th>Статус</th>
        </tr>
    </thead>
    <tbody>
        {% for result in item.results %}
            <tr>
                <td>
                    {% if result.position %}
                        {{ result.position }}
                        {% if result.position == 1 %}🥇
                        {% elif result.position == 2 %}🥈
                        {% elif result.position == 3 %}🥉
                        {% endif %}
                    {% endif %}
                </td>
                <td><strong>{{ result.driver.full_name }}</strong></td>
                <!-- ... остальные поля ... -->
            </tr>
        {% endfor %}
    </tbody>
</table>
```

Медали добавляют наглядности для первых трех мест.

### Формы

Для отображения форм используется `django-crispy-forms`:

```html
{% load crispy_forms_tags %}

<form method="post">
    {% csrf_token %}
    {{ form|crispy }}
    <button type="submit" class="btn btn-primary">Сохранить</button>
</form>
```

Это автоматически применяет стили Bootstrap 5 к форме.

### Пагинация

Стандартный блок пагинации с:

- Кнопками "Первая" и "Последняя"
- Кнопками "Назад" и "Вперед"
- Номерами страниц (показываются ближайшие 3)
- Информацией о текущей странице

```html
<nav aria-label="Навигация">
    <ul class="pagination justify-content-center">
        {% if page_obj.has_previous %}
            <li class="page-item">
                <a class="page-link" href="?page=1">Первая</a>
            </li>
        {% else %}
            <li class="page-item disabled">
                <span class="page-link">Первая</span>
            </li>
        {% endif %}
        
        <!-- Номера страниц -->
        {% for num in page_obj.paginator.page_range %}
            {% if page_obj.number == num %}
                <li class="page-item active">
                    <span class="page-link">{{ num }}</span>
                </li>
            {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
                <li class="page-item">
                    <a class="page-link" href="?page={{ num }}">{{ num }}</a>
                </li>
            {% endif %}
        {% endfor %}
        
        <!-- Аналогично для "Вперед" и "Последняя" -->
    </ul>
</nav>
```

## Сообщения пользователю

Django messages отображаются с помощью Bootstrap alerts:

```html
{% if messages %}
    {% for message in messages %}
        <div class="alert alert-{{ message.tags }} alert-dismissible fade show">
            {{ message }}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    {% endfor %}
{% endif %}
```

Типы сообщений соответствуют классам Bootstrap:

- `success` - зеленый alert
- `warning` - желтый alert
- `info` - синий alert
- `error` - красный alert (в Django это `danger`)

## Защита CSRF

Все формы содержат токен CSRF для защиты от подделки запросов:

```html
<form method="post">
    {% csrf_token %}
    <!-- поля формы -->
</form>
```

Это обязательное требование Django для POST запросов.

## Фильтры шаблонов

Django предоставляет фильтры для форматирования данных:

```html
<!-- Форматирование даты -->
{{ race.date|date:"d.m.Y" }}

<!-- Обрезка текста -->
{{ race.description|truncatechars:100 }}

<!-- Преобразование переносов строк в <br> -->
{{ comment.text|linebreaks }}

<!-- Значение по умолчанию -->
{{ driver.team.name|default:"—" }}
```

## Условия и циклы

В шаблонах можно использовать логику:

```html
<!-- Условие -->
{% if user.is_authenticated %}
    <p>Привет, {{ user.username }}!</p>
{% else %}
    <a href="{% url 'login' %}">Войти</a>
{% endif %}

<!-- Цикл -->
{% for race in races %}
    <div>{{ race.title }}</div>
{% empty %}
    <p>Нет гонок</p>
{% endfor %}
```

## Итоги

Представления и шаблоны работают вместе:

1. **Представление** получает данные из базы
2. **Представление** обрабатывает формы и логику
3. **Представление** передает данные в шаблон
4. **Шаблон** отображает данные в HTML

Я использовала CBV для стандартных операций и FBV для специфичной логики. Все шаблоны наследуются от базового, используют Bootstrap 5 и crispy-forms для красивого отображения.



