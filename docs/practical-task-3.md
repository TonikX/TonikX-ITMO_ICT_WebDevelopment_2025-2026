# Документация: Задание 2.3
## Расширение модели пользователя через AbstractUser

---

## Описание задания

### Задача
Сделать "Владельца автомобиля" пользователем и расширить модель пользователя его атрибутами, так, чтобы о нем хранилась следующая информация:
- **Номер паспорта**
- **Домашний адрес**
- **Национальность**

### Требования
- Отобразить новые поля пользователя в Django Admin
- Отредактировать код из предыдущих работ для вывода информации о пользователях
- Реализовать интерфейс создания пользователя с новыми атрибутами

### Реализация
Использовать наследование от `AbstractUser` - базового класса Django для создания кастомных пользователей.

---

## Расширение модели CarOwner

### Шаг 1: Изменение модели на наследование от AbstractUser

Модель `CarOwner` была изменена с обычной модели на кастомную модель пользователя:

**Было:**
```python
from django.db import models

class CarOwner(models.Model):
    """Автовладелец"""
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    birth_date = models.DateField(null=True, blank=True)
    cars = models.ManyToManyField('Car', through='Ownership', related_name='owners')
```

**Стало:**
```python
from django.db import models
from django.contrib.auth.models import AbstractUser

class CarOwner(AbstractUser):
    """Автовладелец - пользователь Django с расширенными атрибутами"""
    # Дополнительные поля к стандартным полям User
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    passport_number = models.CharField(max_length=20, null=True, blank=True, verbose_name="Номер паспорта")
    home_address = models.TextField(null=True, blank=True, verbose_name="Домашний адрес")
    nationality = models.CharField(max_length=50, null=True, blank=True, verbose_name="Национальность")
    
    # Связь многие-ко-многим с автомобилями через промежуточную таблицу Ownership
    cars = models.ManyToManyField('Car', through='Ownership', related_name='owners')
    
    class Meta:
        verbose_name = "Автовладелец"
        verbose_name_plural = "Автовладельцы"
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"
```

### Что такое AbstractUser?

`AbstractUser` - это абстрактный класс Django, который предоставляет полную реализацию модели пользователя со следующими полями:

**Основные поля:**
- `username` - имя пользователя (логин)
- `password` - пароль (хранится в зашифрованном виде)
- `email` - адрес электронной почты
- `first_name` - имя
- `last_name` - фамилия

**Поля статуса:**
- `is_staff` - доступ к админ-панели
- `is_superuser` - права суперпользователя
- `is_active` - активен ли аккаунт

**Временные метки:**
- `date_joined` - дата регистрации
- `last_login` - последний вход

**Связи:**
- `groups` - группы пользователя (Many-to-Many)
- `user_permissions` - индивидуальные права (Many-to-Many)

### Добавленные кастомные поля

К стандартным полям User добавлены:

| Поле | Тип | Описание |
|------|-----|----------|
| `birth_date` | DateField | Дата рождения (опционально) |
| `passport_number` | CharField(20) | Номер паспорта (опционально) |
| `home_address` | TextField | Домашний адрес (опционально) |
| `nationality` | CharField(50) | Национальность (опционально) |

Все новые поля имеют параметры:
- `null=True` - может быть NULL в базе данных
- `blank=True` - необязательно для заполнения в формах
- `verbose_name` - русское название для админ-панели

**Результат:**
- CarOwner теперь полноценный пользователь Django
- Поддерживается аутентификация и авторизация
- Работают права доступа и группы
- Сохранены все прежние поля и связи

---

## Настройка кастомной модели пользователя

### Шаг 2: Указание кастомной модели в настройках

В файле `task1/settings.py` добавлена настройка `AUTH_USER_MODEL`:

```python
# Кастомная модель пользователя
AUTH_USER_MODEL = 'task1.CarOwner'
```

### Назначение AUTH_USER_MODEL

Эта настройка сообщает Django, какую модель использовать вместо стандартной модели `User`:

**Что это дает:**
1. Django использует `CarOwner` для аутентификации
2. `request.user` будет объектом `CarOwner`
3. Все системы прав доступа работают с `CarOwner`
4. Foreign Key на User автоматически указывает на `CarOwner`

**Важно:** Эту настройку нужно указать до первой миграции проекта. При изменении модели пользователя в существующем проекте необходимо пересоздать базу данных.

**Формат значения:**
```python
AUTH_USER_MODEL = 'название_приложения.НазваниеМодели'
```

В нашем случае:
- Приложение: `task1`
- Модель: `CarOwner`

**Результат:**
- Django распознает `CarOwner` как модель пользователя
- Система аутентификации использует наши поля
- Админ-панель работает с расширенной моделью

---

## Обновление административной панели

### Шаг 3: Настройка админки для кастомного пользователя

Файл `task1/admin.py` был обновлен для работы с кастомной моделью пользователя:

**Было:**
```python
from django.contrib import admin
from .models import CarOwner

@admin.register(CarOwner)
class CarOwnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'first_name', 'birth_date')
    search_fields = ('last_name', 'first_name')
```

**Стало:**
```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CarOwner

@admin.register(CarOwner)
class CarOwnerAdmin(UserAdmin):
    """Админка для владельцев автомобилей (расширенная модель User)"""
    list_display = ('username', 'email', 'first_name', 'last_name', 'passport_number', 'nationality', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'passport_number')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'nationality')
    
    # Добавляем наши кастомные поля в fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('birth_date', 'passport_number', 'home_address', 'nationality')
        }),
    )
    
    # Добавляем кастомные поля при создании пользователя
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {
            'fields': ('birth_date', 'passport_number', 'home_address', 'nationality')
        }),
    )
```

### Изменения в админке

#### Наследование от UserAdmin

Теперь `CarOwnerAdmin` наследуется от `UserAdmin` вместо `ModelAdmin`:

**UserAdmin предоставляет:**
- Форму для создания пользователя с паролем
- Форму редактирования без прямого доступа к паролю
- Форму смены пароля
- Группировку полей в fieldsets
- Управление правами и группами

#### list_display

Отображаемые в списке поля:
- `username` - логин пользователя
- `email` - электронная почта
- `first_name`, `last_name` - имя и фамилия
- `passport_number` - номер паспорта (кастомное)
- `nationality` - национальность (кастомное)
- `is_staff` - статус персонала

#### search_fields

Поля для поиска:
- По логину (`username`)
- По имени и фамилии
- По email
- По номеру паспорта

#### list_filter

Фильтры в боковой панели:
- По статусу персонала
- По статусу суперпользователя
- По активности аккаунта
- По национальности

#### fieldsets

`fieldsets` определяет, как поля группируются на странице редактирования:

```python
fieldsets = UserAdmin.fieldsets + (
    ('Дополнительная информация', {
        'fields': ('birth_date', 'passport_number', 'home_address', 'nationality')
    }),
)
```

**Структура:**
- Берем стандартные fieldsets от UserAdmin
- Добавляем (`+`) новую секцию
- Секция "Дополнительная информация" содержит наши кастомные поля

**Стандартные секции UserAdmin:**
1. Основная информация (username, password)
2. Personal info (first_name, last_name, email)
3. Permissions (is_active, is_staff, is_superuser, groups, permissions)
4. Important dates (last_login, date_joined)

#### add_fieldsets

Определяет поля при создании нового пользователя:

```python
add_fieldsets = UserAdmin.add_fieldsets + (
    ('Дополнительная информация', {
        'fields': ('birth_date', 'passport_number', 'home_address', 'nationality')
    }),
)
```

При создании пользователя будут доступны:
- Стандартные поля (username, password1, password2)
- Наши кастомные поля

**Результат:**
- Полнофункциональная админка для пользователей
- Все стандартные возможности User
- Доступ к нашим кастомным полям
- Удобная группировка информации

---

## Создание формы регистрации

### Шаг 4: Форма регистрации с расширенными полями

В файле `task1/forms.py` создана форма регистрации на основе `UserCreationForm`:

```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CarOwner

class CarOwnerRegistrationForm(UserCreationForm):
    """Форма регистрации владельца автомобиля с расширенными полями"""
    
    class Meta:
        model = CarOwner
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2',
                  'birth_date', 'passport_number', 'home_address', 'nationality']
        labels = {
            'username': 'Имя пользователя',
            'email': 'Email',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'birth_date': 'Дата рождения',
            'passport_number': 'Номер паспорта',
            'home_address': 'Домашний адрес',
            'nationality': 'Национальность',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ivan_ivanov'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иван'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иванов'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'passport_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234 567890'}),
            'home_address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'г. Москва, ул. Ленина, д. 1, кв. 10', 'rows': 3}),
            'nationality': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Российская Федерация'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем классы для полей паролей
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
```

### Что такое UserCreationForm?

`UserCreationForm` - встроенная форма Django для создания пользователей:

**Предоставляет:**
- Поля `password1` и `password2` для ввода пароля дважды
- Валидацию совпадения паролей
- Автоматическое хеширование пароля при сохранении
- Проверку сложности пароля

### Поля формы

#### Стандартные поля User:
- `username` - уникальное имя пользователя (логин)
- `email` - электронная почта
- `first_name` - имя
- `last_name` - фамилия
- `password1` - пароль
- `password2` - подтверждение пароля

#### Кастомные поля:
- `birth_date` - дата рождения (виджет выбора даты)
- `passport_number` - номер паспорта
- `home_address` - текстовое поле (Textarea) для адреса
- `nationality` - национальность

### Настройка виджетов

Каждое поле имеет настроенный HTML-виджет:

**TextInput** - однострочное текстовое поле:
```python
'username': forms.TextInput(attrs={
    'class': 'form-control',        # CSS-класс для стилизации
    'placeholder': 'ivan_ivanov'    # Подсказка в поле
})
```

**EmailInput** - поле для email с валидацией:
```python
'email': forms.EmailInput(attrs={
    'class': 'form-control',
    'placeholder': 'email@example.com'
})
```

**DateInput** - выбор даты:
```python
'birth_date': forms.DateInput(attrs={
    'class': 'form-control',
    'type': 'date'  # HTML5 date picker
})
```

**Textarea** - многострочное текстовое поле:
```python
'home_address': forms.Textarea(attrs={
    'class': 'form-control',
    'placeholder': 'г. Москва, ул. Ленина, д. 1, кв. 10',
    'rows': 3  # Высота поля
})
```

### Метод __init__

Переопределяем `__init__` для настройки полей паролей:

```python
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['password1'].widget.attrs.update({'class': 'form-control'})
    self.fields['password2'].widget.attrs.update({'class': 'form-control'})
```

**Почему так?**
Поля `password1` и `password2` определены в родительском классе `UserCreationForm`, поэтому мы не можем настроить их через `widgets` в Meta. Вместо этого обновляем атрибуты виджетов в `__init__`.

**Результат:**
- Полная форма регистрации со всеми полями
- Красивое оформление с помощью CSS-классов
- Подсказки для пользователя (placeholders)
- Автоматическая валидация

---

## Обновление представлений

### Шаг 5: Изменение view для регистрации

В файле `task1/views.py` обновлена функция создания владельца:

**Было:**
```python
from .forms import CarOwnerForm

def create_owner(request):
    if request.method == 'POST':
        form = CarOwnerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('owners_list')
    else:
        form = CarOwnerForm()
    
    return render(request, 'owner_form.html', {'form': form, 'title': 'Добавить владельца'})
```

**Стало:**
```python
from django.contrib import messages
from .forms import CarOwnerRegistrationForm

def create_owner(request):
    """Function-based view для регистрации нового владельца (пользователя) через форму"""
    if request.method == 'POST':
        form = CarOwnerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Пользователь {user.username} успешно зарегистрирован!')
            return redirect('owners_list')
    else:
        form = CarOwnerRegistrationForm()
    
    return render(request, 'owner_form.html', {'form': form, 'title': 'Регистрация владельца'})
```

### Изменения

#### 1. Использование новой формы

Заменена `CarOwnerForm` на `CarOwnerRegistrationForm`:
- Включает поля паролей
- Обрабатывает хеширование пароля
- Валидирует все пользовательские поля

#### 2. Добавлены сообщения

Импортирован модуль `messages`:
```python
from django.contrib import messages
```

После успешной регистрации показывается сообщение:
```python
messages.success(request, f'Пользователь {user.username} успешно зарегистрирован!')
```

**Типы сообщений:**
- `messages.success()` - успех (зеленый)
- `messages.info()` - информация (синий)
- `messages.warning()` - предупреждение (желтый)
- `messages.error()` - ошибка (красный)

#### 3. Обновлен заголовок

Изменен title с "Добавить владельца" на "Регистрация владельца", что точнее отражает суть операции - создание пользователя с учетными данными.

**Результат:**
- Регистрация полноценного пользователя
- Автоматическое хеширование пароля
- Уведомление об успешной регистрации
- Перенаправление на список владельцев

---

## Обновление шаблонов

### Шаг 6: Обновление списка владельцев

Файл `templates/owners_list.html` обновлен для отображения пользовательских полей:

**Заголовки таблицы:**
```html
<tr>
    <th>ID</th>
    <th>Username</th>
    <th>Фамилия</th>
    <th>Имя</th>
    <th>Email</th>
    <th>Паспорт</th>
    <th>Национальность</th>
    <th>Действия</th>
</tr>
```

**Строки таблицы:**
```html
{% for owner in owners %}
<tr>
    <td>{{ owner.id }}</td>
    <td>{{ owner.username }}</td>
    <td>{{ owner.last_name }}</td>
    <td>{{ owner.first_name }}</td>
    <td>{{ owner.email|default:"—" }}</td>
    <td>{{ owner.passport_number|default:"—" }}</td>
    <td>{{ owner.nationality|default:"—" }}</td>
    <td><a href="/owner/{{ owner.id }}/">Подробнее</a></td>
</tr>
{% endfor %}
```

**Изменения:**
- Добавлен столбец `Username` - логин пользователя
- Добавлен столбец `Email` - электронная почта
- Добавлен столбец `Паспорт` - номер паспорта
- Добавлен столбец `Национальность`
- Убрана дата рождения из списка (отображается в деталях)

### Шаг 7: Обновление страницы деталей владельца

Файл `templates/owner_detail.html` разделен на секции:

**Основная информация:**
```html
<div class="info-block">
    <h2>Основная информация</h2>
    <div class="info-item"><strong>ID:</strong> {{ owner.id }}</div>
    <div class="info-item"><strong>Username:</strong> {{ owner.username }}</div>
    <div class="info-item"><strong>Email:</strong> {{ owner.email|default:"Не указан" }}</div>
    <div class="info-item"><strong>Фамилия:</strong> {{ owner.last_name }}</div>
    <div class="info-item"><strong>Имя:</strong> {{ owner.first_name }}</div>
    <div class="info-item"><strong>Дата рождения:</strong> {{ owner.birth_date|default:"Не указана" }}</div>
</div>
```

**Документы и адрес:**
```html
<div class="info-block">
    <h2>Документы и адрес</h2>
    <div class="info-item"><strong>Номер паспорта:</strong> {{ owner.passport_number|default:"Не указан" }}</div>
    <div class="info-item"><strong>Домашний адрес:</strong> {{ owner.home_address|default:"Не указан" }}</div>
    <div class="info-item"><strong>Национальность:</strong> {{ owner.nationality|default:"Не указана" }}</div>
</div>
```

**Структура информации:**
1. Основная информация (User поля)
2. Документы и адрес (кастомные поля)
3. Автомобили владельца (связь ManyToMany)
4. Водительские удостоверения (связь ForeignKey)

### Шаг 8: Обновление формы регистрации

В `templates/owner_form.html` добавлено отображение сообщений:

```html
{% if messages %}
<div style="background-color: #d4edda; border: 1px solid #c3e6cb; color: #155724; padding: 12px; border-radius: 4px; margin-bottom: 20px;">
    {% for message in messages %}
    <p style="margin: 0;">{{ message }}</p>
    {% endfor %}
</div>
{% endif %}
```

**Назначение:**
- Отображает сообщения от Django messages framework
- Зеленый фон для успешных сообщений
- Показывается над формой

**Результат:**
- Вся информация о пользователе организована и доступна
- Четкое разделение на секции
- Отображение всех стандартных и кастомных полей
- Уведомления об успешных действиях

---

## Миграции базы данных

### Шаг 9: Пересоздание базы данных

Поскольку изменение модели пользователя - критичная операция, база данных была пересоздана:

#### Удаление старой базы и миграций

```bash
rm -f db.sqlite3
rm -rf task1/migrations/*.py
touch task1/migrations/__init__.py
```

**Почему нужно удалять?**
- Изменение `AUTH_USER_MODEL` несовместимо с существующей БД
- Django не может мигрировать данные между разными моделями User
- Проще пересоздать БД, чем писать сложные миграции данных

#### Создание новых миграций

```bash
python manage.py makemigrations
```

**Вывод:**
```
Migrations for 'task1':
  task1/migrations/0001_initial.py
    + Create model Car
    + Create model CarOwner
    + Create model DriverLicense
    + Create model Ownership
    + Add field cars to carowner
```

**Что создается:**
- Таблица `task1_carowner` с полями User + кастомными полями
- Таблица `task1_car` для автомобилей
- Таблица `task1_driverlicense` для водительских удостоверений
- Таблица `task1_ownership` для связи владельцев и автомобилей
- Промежуточная таблица для ManyToMany связи

#### Применение миграций

```bash
python manage.py migrate
```

**Применяются миграции:**
1. `contenttypes` - система типов контента
2. `auth` - система аутентификации
3. `task1` - наше приложение
4. `admin` - административная панель
5. `sessions` - система сессий

**Результат:**
- Создана новая база данных
- Таблица пользователей использует нашу модель `CarOwner`
- Все связи настроены корректно

### Шаг 10: Создание суперпользователя

После пересоздания БД необходимо создать нового администратора:

```bash
python manage.py createsuperuser --username admin --email admin@example.com --no-input
python manage.py shell -c "from task1.models import CarOwner; u = CarOwner.objects.get(username='admin'); u.set_password('admin'); u.save()"
```

**Учетные данные:**
- Логин: `admin`
- Пароль: `admin`
- Email: `admin@example.com`

**Результат:**
- Доступ к админ-панели восстановлен
- Можно управлять всеми данными

---

## Итоговая функциональность

### Реализованные возможности

#### Модель CarOwner (расширенный User)

**Стандартные поля User:**
- ✅ `username` - логин для входа
- ✅ `password` - зашифрованный пароль
- ✅ `email` - электронная почта
- ✅ `first_name` - имя
- ✅ `last_name` - фамилия
- ✅ `is_staff` - доступ к админке
- ✅ `is_superuser` - права суперпользователя
- ✅ `is_active` - активность аккаунта
- ✅ `date_joined` - дата регистрации
- ✅ `last_login` - последний вход
- ✅ `groups` - группы пользователя
- ✅ `user_permissions` - права доступа

**Кастомные поля:**
- ✅ `birth_date` - дата рождения
- ✅ `passport_number` - номер паспорта
- ✅ `home_address` - домашний адрес
- ✅ `nationality` - национальность

**Связи:**
- ✅ `cars` - автомобили владельца (ManyToMany)
- ✅ `licenses` - водительские удостоверения (reverse ForeignKey)
- ✅ `ownerships` - история владения (reverse ForeignKey)

#### Административная панель

✅ **Список пользователей:**
- Username, email, имя, фамилия
- Номер паспорта, национальность
- Статус персонала

✅ **Редактирование пользователя:**
- Все стандартные поля User
- Секция "Дополнительная информация" с кастомными полями
- Управление правами и группами

✅ **Создание пользователя:**
- Форма с username и паролями
- Кастомные поля доступны при создании

✅ **Поиск и фильтрация:**
- Поиск по username, имени, email, паспорту
- Фильтры по статусу и национальности

#### Регистрация пользователей

✅ **Форма регистрации:**
- Все обязательные поля User
- Пароль с подтверждением
- Все кастомные поля
- Красивое оформление

✅ **Валидация:**
- Уникальность username
- Проверка сложности пароля
- Совпадение password1 и password2
- Формат email

✅ **После регистрации:**
- Автоматическое хеширование пароля
- Сообщение об успехе
- Перенаправление на список

#### Отображение данных

✅ **Список владельцев:**
- ID, username, ФИО
- Email, паспорт, национальность
- Ссылка на детальную страницу

✅ **Детали владельца:**
- Основная информация (User поля)
- Документы и адрес (кастомные поля)
- Автомобили владельца
- Водительские удостоверения

### Доступные URL-адреса

**Административная панель:**
- http://127.0.0.1:8000/admin/ - управление пользователями и данными

**Владельцы:**
- http://127.0.0.1:8000/owners/ - список всех владельцев
- http://127.0.0.1:8000/owner/create/ - регистрация нового владельца
- http://127.0.0.1:8000/owner/`<id>`/ - детали владельца

**Автомобили:**
- http://127.0.0.1:8000/cars/ - список автомобилей
- http://127.0.0.1:8000/car/create/ - добавить автомобиль
- http://127.0.0.1:8000/car/`<id>`/ - детали автомобиля
- http://127.0.0.1:8000/car/`<id>`/update/ - редактировать
- http://127.0.0.1:8000/car/`<id>`/delete/ - удалить

---

## Преимущества использования AbstractUser

### Встроенная функциональность

✅ **Аутентификация:**
- Вход в систему (`login`)
- Выход из системы (`logout`)
- Проверка пароля
- Смена пароля

✅ **Авторизация:**
- Система прав доступа
- Группы пользователей
- Проверка прав через декораторы
- Миксины для class-based views

✅ **Безопасность:**
- Хеширование паролей (PBKDF2 по умолчанию)
- Защита от brute-force атак
- Управление сессиями
- CSRF-защита

### Расширяемость

✅ **Добавление полей:**
```python
class CarOwner(AbstractUser):
    # Просто добавляем нужные поля
    passport_number = models.CharField(...)
```

✅ **Сохранение всех возможностей User:**
- Не нужно переписывать логику аутентификации
- Совместимость со всеми Django-приложениями
- Работают все middleware и декораторы

✅ **Кастомизация поведения:**
```python
class CarOwner(AbstractUser):
    def get_full_name(self):
        # Можно переопределять методы
        return f"{self.first_name} {self.last_name} ({self.nationality})"
```

### Интеграция с Django

✅ **Автоматическая интеграция:**
- `request.user` - текущий пользователь
- `@login_required` - требование авторизации
- `LoginRequiredMixin` - для CBV
- `user.is_authenticated` - проверка аутентификации

✅ **Совместимость:**
- Django Admin использует модель автоматически
- Django Rest Framework работает "из коробки"
- Все сторонние пакеты для аутентификации совместимы

---

## Пример использования

### Регистрация нового владельца

**Шаг 1:** Перейти на страницу регистрации  
→ http://127.0.0.1:8000/owner/create/

**Шаг 2:** Заполнить форму
- Username: `ivan_petrov`
- Email: `ivan@example.com`
- Имя: `Иван`
- Фамилия: `Петров`
- Password: `SecurePass123`
- Password (again): `SecurePass123`
- Дата рождения: `1990-05-15`
- Номер паспорта: `1234 567890`
- Домашний адрес: `г. Москва, ул. Ленина, д. 5, кв. 42`
- Национальность: `Российская Федерация`

**Шаг 3:** Нажать "Сохранить"

**Результат:**
- Пользователь создан и сохранен в БД
- Пароль автоматически зашифрован
- Показано сообщение: "Пользователь ivan_petrov успешно зарегистрирован!"
- Перенаправление на список владельцев
- Новый владелец появился в списке

### Просмотр информации через админку

**Шаг 1:** Войти в админку  
→ http://127.0.0.1:8000/admin/  
(admin / admin)

**Шаг 2:** Открыть раздел "Автовладельцы"

**Шаг 3:** Выбрать пользователя

**Видим:**
- Все стандартные поля User
- Секцию "Дополнительная информация" с нашими полями
- Историю изменений
- Права и группы

### Создание данных через админку

Через админ-панель можно:
1. Создать владельцев (пользователей)
2. Создать автомобили
3. Создать водительские удостоверения
4. Связать владельцев с автомобилями через записи Ownership

---

## Полезные команды

### Работа с пользователями

```bash
# Создать суперпользователя
python manage.py createsuperuser

# Создать обычного пользователя через shell
python manage.py shell
```

```python
from task1.models import CarOwner

# Создание пользователя
user = CarOwner.objects.create_user(
    username='testuser',
    email='test@example.com',
    password='testpass123',
    first_name='Test',
    last_name='User',
    passport_number='9999 888888',
    nationality='Test Country'
)

# Получить пользователя
user = CarOwner.objects.get(username='testuser')

# Проверить пароль
user.check_password('testpass123')  # True

# Сменить пароль
user.set_password('newpass123')
user.save()

# Дать права админа
user.is_staff = True
user.is_superuser = True
user.save()
```

### Работа с миграциями

```bash
# Показать SQL для миграции
python manage.py sqlmigrate task1 0001

# Откатить миграции
python manage.py migrate task1 zero

# Показать статус миграций
python manage.py showmigrations
```

---

## Заключение

В результате выполнения задания 2.3 успешно реализовано:

### Основные достижения

✅ **Интеграция с системой пользователей Django:**
- CarOwner теперь полноценный User
- Поддержка аутентификации и авторизации
- Работа с правами доступа

✅ **Расширенная модель пользователя:**
- Все стандартные поля User
- Кастомные поля: паспорт, адрес, национальность
- Сохранены связи с автомобилями и удостоверениями

✅ **Административная панель:**
- Расширенная админка на базе UserAdmin
- Отображение всех полей
- Удобная группировка информации

✅ **Форма регистрации:**
- Полная регистрация с паролем
- Все кастомные поля
- Валидация и защита

✅ **Обновленные шаблоны:**
- Отображение пользовательских данных
- Организация по секциям
- Сообщения об успешных действиях

### Возможности для развития

Созданная система готова для добавления:
- Авторизации и личных кабинетов
- Системы прав доступа
- Ограничения доступа к автомобилям
- Истории действий пользователей
- Социальной аутентификации
- REST API с аутентификацией

Приложение полностью готово к использованию с полноценной системой пользователей!

