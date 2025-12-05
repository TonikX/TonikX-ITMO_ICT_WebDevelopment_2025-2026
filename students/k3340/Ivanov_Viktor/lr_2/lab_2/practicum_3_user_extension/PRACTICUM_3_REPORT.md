# Отчет по Практическому заданию №3
## Расширение пользовательской модели

**Дата выполнения:** 15 октября 2025  
**Автор:** Иванов Виктор

---

## 📋 Задание

**Цель:** Расширить пользовательскую модель Django, сделав "Владельца автомобиля" пользователем системы.

**Требования:**
1. Использовать подход AbstractUser для расширения модели пользователя
2. Добавить новые атрибуты:
   - Номер паспорта
   - Домашний адрес
   - Национальность
3. Отобразить новые поля пользователя в Django Admin
4. Отредактировать код из предыдущих работ для работы с пользователями
5. Реализовать интерфейс создания пользователя с новыми атрибутами

---

## ✅ Выполненные задачи

### 1. Создание кастомной модели User

**Файл:** `project_first_app/models.py`

Создана модель `User`, наследующая `AbstractUser`:

```python
class User(AbstractUser):
    """Расширенная модель пользователя (владелец автомобиля)"""
    # Стандартные поля AbstractUser: username, first_name, last_name, email, password
    
    # Дополнительные поля из старой модели Avtovladelec
    patronymic = models.CharField(max_length=30, blank=True, null=True, verbose_name='Отчество')
    data_rozhdeniya = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    
    # Новые поля из задания
    passport_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Номер паспорта')
    home_address = models.TextField(blank=True, null=True, verbose_name='Домашний адрес')
    nationality = models.CharField(max_length=50, blank=True, null=True, verbose_name='Национальность')
    
    # Связь многие-ко-многим с автомобилями
    avtomobili = models.ManyToManyField(
        'Avtomobil',
        through='Vladenie',
        related_name='vladelcy',
        verbose_name='Автомобили'
    )
```

**Добавленные поля:**
- ✅ `patronymic` - отчество (дополнительное поле)
- ✅ `data_rozhdeniya` - дата рождения (из старой модели)
- ✅ `passport_number` - номер паспорта (новое поле)
- ✅ `home_address` - домашний адрес (новое поле)
- ✅ `nationality` - национальность (новое поле)

---

### 2. Настройка AUTH_USER_MODEL

**Файл:** `django_project_ivanov/settings.py`

Добавлена настройка кастомной модели пользователя:

```python
AUTH_USER_MODEL = 'project_first_app.User'
```

---

### 3. Обновление связанных моделей

**Файлы:** `project_first_app/models.py`

Обновлены модели для использования `settings.AUTH_USER_MODEL`:

#### Модель Vladenie:
```python
id_vladelca = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    null=True,
    verbose_name='Владелец'
)
```

#### Модель Voditelskoe_udostoverenie:
```python
id_vladelca = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    null=False,
    verbose_name='Владелец'
)
```

**Удалена старая модель:** `Avtovladelec` полностью заменена на `User`

---

### 4. Настройка Django Admin

**Файл:** `project_first_app/admin.py`

Создана кастомная админка для расширенной модели пользователя:

```python
class CustomUserAdmin(BaseUserAdmin):
    """Админка для расширенной модели User"""
    
    # Поля для отображения в списке
    list_display = ('username', 'email', 'first_name', 'last_name', 'passport_number', 'nationality', 'is_staff')
    
    # Добавляем новые поля в разделы админки
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('patronymic', 'data_rozhdeniya', 'passport_number', 'home_address', 'nationality')
        }),
    )
    
    # Поля для создания нового пользователя
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Дополнительная информация', {
            'fields': ('first_name', 'last_name', 'patronymic', 'data_rozhdeniya', 
                      'passport_number', 'home_address', 'nationality', 'email')
        }),
    )
```

**Возможности админки:**
- ✅ Отображение всех новых полей в списке пользователей
- ✅ Редактирование всех полей через админку
- ✅ Создание новых пользователей с расширенными полями
- ✅ Фильтрация по новым полям

---

### 5. Создание формы регистрации

**Файл:** `project_first_app/forms.py`

Создана форма регистрации с новыми полями:

```python
class UserRegistrationForm(UserCreationForm):
    """Форма регистрации пользователя с расширенными полями"""
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'patronymic', 'email', 
                 'data_rozhdeniya', 'passport_number', 'home_address', 'nationality', 
                 'password1', 'password2']
```

**Особенности формы:**
- Наследует от `UserCreationForm` для безопасной регистрации
- Включает все новые поля из задания
- Добавлены CSS-классы для стилизации
- Placeholder'ы для удобства заполнения

---

### 6. Обновление представлений (views)

**Файл:** `project_first_app/views.py`

#### Обновлены функциональные представления:
```python
User = get_user_model()

def owner_list(request):
    """Список всех пользователей-владельцев"""
    context = {}
    context['owners'] = User.objects.all()
    return render(request, 'owner_list.html', context)

def owner_detail(request, owner_id):
    """Информация о пользователе-владельце"""
    try:
        owner = User.objects.get(pk=owner_id)
    except User.DoesNotExist:
        raise Http404("Пользователь не найден")
    return render(request, 'owner_detail.html', {'owner': owner})
```

#### Добавлено представление регистрации:
```python
def owner_create(request):
    """Регистрация нового пользователя-владельца"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            return redirect('owner_list')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'user_registration.html', {'form': form})
```

---

### 7. Создание/обновление шаблонов

#### 7.1. Шаблон регистрации: `user_registration.html`

**Новый файл с полями:**
- Учетные данные (логин, пароли)
- Личные данные (ФИО, email, дата рождения)
- Дополнительная информация (паспорт, адрес, национальность)

**Особенности:**
- Разделение на логические секции
- Информационный блок с инструкциями
- Валидация на стороне клиента
- Красивая стилизация

#### 7.2. Обновлен `owner_detail.html`

Теперь отображает:
- ✅ Логин (username)
- ✅ ФИО (first_name, last_name, patronymic)
- ✅ Email
- ✅ Дата рождения
- ✅ Номер паспорта (новое поле)
- ✅ Домашний адрес (новое поле)
- ✅ Национальность (новое поле)

#### 7.3. Обновлен `owner_list.html`

Теперь показывает:
- ФИО с отчеством
- Логин пользователя
- Email
- Дата рождения
- Национальность

---

### 8. Миграции базы данных

**Выполнено:**
1. Удалена старая база данных
2. Удалены старые миграции
3. Созданы новые миграции с моделью User
4. Применены миграции

**Файл миграции:** `project_first_app/migrations/0001_initial.py`

**Создано:**
- Таблица для расширенной модели User
- Обновлены связи в таблицах Vladenie и Voditelskoe_udostoverenie

---

## 📊 Тестовые данные

### Созданные пользователи:

1. **Admin** (суперпользователь)
   - Логин: admin
   - Пароль: admin

2. **Иванов Петр Сергеевич**
   - Логин: ivanov_p
   - Email: ivanov@example.com
   - Паспорт: 4509 123456
   - Адрес: г. Москва, ул. Ленина, д. 10, кв. 25
   - Национальность: Русский
   - Дата рождения: 15.05.1985

3. **Сидоров Алексей Иванович**
   - Логин: sidorov_a
   - Email: sidorov@example.com
   - Паспорт: 4510 654321
   - Адрес: г. Санкт-Петербург, пр. Невский, д. 45
   - Национальность: Русский
   - Дата рождения: 22.08.1990

4. **Петров Дмитрий**
   - Логин: petrov_d
   - Email: petrov@example.com
   - Паспорт: 4511 789012
   - Адрес: г. Казань, ул. Баумана, д. 15
   - Национальность: Русский
   - Дата рождения: 10.03.1988

---

## 🌐 Доступные URL-адреса

### Страницы пользователей:
- `http://127.0.0.1:8000/` - Список всех пользователей (владельцев)
- `http://127.0.0.1:8000/owner/2/` - Детальная информация о пользователе
- `http://127.0.0.1:8000/owner/create/` - Регистрация нового пользователя

### Админ-панель:
- `http://127.0.0.1:8000/admin/` - Django Admin с расширенной моделью User
  - Логин: admin
  - Пароль: admin

### Автомобили:
- `http://127.0.0.1:8000/avtomobil/` - Список автомобилей (работает как раньше)

---

## 🎯 Результаты

### ✅ Все требования выполнены:

1. ✅ **Использован подход AbstractUser** для расширения модели
2. ✅ **Добавлены новые атрибуты:**
   - Номер паспорта (passport_number)
   - Домашний адрес (home_address)
   - Национальность (nationality)
3. ✅ **Новые поля отображаются в Django Admin:**
   - В списке пользователей
   - При редактировании
   - При создании новых пользователей
4. ✅ **Код из предыдущих работ обновлен:**
   - Все представления работают с User
   - Все шаблоны обновлены
   - Связи в моделях обновлены
5. ✅ **Реализован интерфейс регистрации:**
   - Форма с всеми новыми атрибутами
   - Валидация данных
   - Автоматический вход после регистрации

---

## 🔑 Преимущества выбранного подхода (AbstractUser)

### Почему AbstractUser, а не другие способы?

**1. Proxy модель** ❌ - Не подходит, так как не позволяет добавлять новые поля

**2. OneToOneField (User Profile)** ⚠️ - Возможно, но требует дополнительных запросов к БД

**3. AbstractBaseUser** ⚠️ - Слишком сложно, требует переопределения всей аутентификации

**4. AbstractUser** ✅ - **ИДЕАЛЬНЫЙ ВЫБОР:**
- Сохраняет всю стандартную аутентификацию Django
- Позволяет легко добавлять новые поля
- Не требует дополнительных запросов
- Интегрируется с Django Admin
- Работает со всеми стандартными view и forms

---

## 📁 Измененные файлы

### Модели:
- ✏️ `project_first_app/models.py` - Создан User, обновлены связи

### Настройки:
- ✏️ `django_project_ivanov/settings.py` - Добавлен AUTH_USER_MODEL

### Админка:
- ✏️ `project_first_app/admin.py` - Кастомная админка для User

### Формы:
- ✏️ `project_first_app/forms.py` - UserRegistrationForm

### Представления:
- ✏️ `project_first_app/views.py` - Обновлены для работы с User

### Шаблоны:
- ✏️ `templates/owner_list.html` - Обновлен для User
- ✏️ `templates/owner_detail.html` - Обновлен для User
- ➕ `templates/user_registration.html` - Новый шаблон регистрации

### Миграции:
- ➕ `project_first_app/migrations/0001_initial.py` - Новая миграция с User

---

## 🧪 Тестирование

### Проверено:
- ✅ Список пользователей отображается корректно
- ✅ Детальная информация показывает все новые поля
- ✅ Регистрация работает с валидацией
- ✅ Админ-панель отображает все поля
- ✅ Создание пользователей через админку
- ✅ Редактирование пользователей
- ✅ Автомобили связываются с пользователями

---

## 📝 Выводы

**Практическое задание №3 выполнено полностью!**

Реализована полноценная система расширенной аутентификации с дополнительными полями:
- Номер паспорта
- Домашний адрес
- Национальность

Владельцы автомобилей теперь являются полноценными пользователями системы с возможностью:
- Регистрации через веб-интерфейс
- Аутентификации
- Управления через админ-панель
- Просмотра информации с расширенными данными

---

**Дата завершения:** 15 октября 2025  
**Статус:** ✅ ВЫПОЛНЕНО

