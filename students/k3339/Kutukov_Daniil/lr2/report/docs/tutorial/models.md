# Модели данных - Tutorial

## 📋 Обзор

В проекте используются 4 основные модели:

1. **User** - владельцы автомобилей
2. **Car** - автомобили
3. **Ownership** - владение автомобилями
4. **DriverLicense** - водительские удостоверения

## 👤 User (Владелец автомобиля)

Расширенная модель пользователя на основе `AbstractUser`.

```python
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    passport_number = models.CharField(
        max_length=20, 
        verbose_name="Номер паспорта",
        blank=True,
        null=True
    )
    home_address = models.TextField(
        verbose_name="Домашний адрес",
        blank=True,
        null=True
    )
    nationality = models.CharField(
        max_length=50,
        verbose_name="Национальность",
        blank=True,
        null=True
    )
    birth_date = models.DateField(
        verbose_name="Дата рождения",
        blank=True,
        null=True
    )
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.username
    
    class Meta:
        verbose_name = "Владелец автомобиля"
        verbose_name_plural = "Владельцы автомобилей"
```

### Поля

| Поле | Тип | Описание |
|------|-----|----------|
| `username` | CharField | Имя пользователя (наследуется) |
| `email` | EmailField | Email адрес (наследуется) |
| `first_name` | CharField | Имя (наследуется) |
| `last_name` | CharField | Фамилия (наследуется) |
| `passport_number` | CharField | Номер паспорта |
| `home_address` | TextField | Домашний адрес |
| `nationality` | CharField | Национальность |
| `birth_date` | DateField | Дата рождения |

## 🚗 Car (Автомобиль)

Модель для хранения информации об автомобилях.

```python
class Car(models.Model):
    brand = models.CharField(max_length=30, verbose_name="Марка")
    model = models.CharField(max_length=30, verbose_name="Модель")
    color = models.CharField(max_length=30, verbose_name="Цвет")
    state_number = models.CharField(
        max_length=10, 
        verbose_name="Государственный номер",
        validators=[MinLengthValidator(1), MaxLengthValidator(10)]
    )
    
    def __str__(self):
        return f"{self.brand} {self.model} ({self.state_number})"
    
    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"
```

### Поля

| Поле | Тип | Описание |
|------|-----|----------|
| `brand` | CharField | Марка автомобиля (max 30) |
| `model` | CharField | Модель автомобиля (max 30) |
| `color` | CharField | Цвет (max 30) |
| `state_number` | CharField | Гос. номер (1-10 символов) |

### Примеры

```python
Car.objects.create(
    brand="Toyota",
    model="Camry",
    color="Черный",
    state_number="А123БВ777"
)
```

## 🤝 Ownership (Владение)

Ассоциативная модель связи владельца и автомобиля.

```python
class Ownership(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        verbose_name="Владелец"
    )
    car = models.ForeignKey(
        Car, 
        on_delete=models.CASCADE, 
        verbose_name="Автомобиль"
    )
    start_date = models.DateField(
        verbose_name="Дата начала владения"
    )
    end_date = models.DateField(
        null=True, 
        blank=True, 
        verbose_name="Дата окончания владения"
    )
    
    def __str__(self):
        return f"{self.owner} владеет {self.car} с {self.start_date}"
    
    class Meta:
        verbose_name = "Владение"
        verbose_name_plural = "Владения"
```

### Поля

| Поле | Тип | Описание |
|------|-----|----------|
| `owner` | ForeignKey(User) | Владелец |
| `car` | ForeignKey(Car) | Автомобиль |
| `start_date` | DateField | Дата начала владения |
| `end_date` | DateField | Дата окончания (опционально) |

### Логика

- Текущее владение: `end_date = None`
- Прошлое владение: `end_date` заполнена

## 🪪 DriverLicense (Водительское удостоверение)

Модель водительских удостоверений.

```python
class DriverLicense(models.Model):
    LICENSE_TYPES = [
        ('A', 'Категория A'),
        ('B', 'Категория B'),
        ('C', 'Категория C'),
        ('D', 'Категория D'),
    ]
    
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        verbose_name="Владелец"
    )
    license_number = models.CharField(
        max_length=10, 
        verbose_name="Номер удостоверения"
    )
    license_type = models.CharField(
        max_length=1, 
        choices=LICENSE_TYPES, 
        verbose_name="Тип удостоверения"
    )
    issue_date = models.DateField(
        verbose_name="Дата выдачи"
    )
    
    def __str__(self):
        return f"Удостоверение {self.license_number} ({self.get_license_type_display()})"
    
    class Meta:
        verbose_name = "Водительское удостоверение"
        verbose_name_plural = "Водительские удостоверения"
```

### Поля

| Поле | Тип | Описание |
|------|-----|----------|
| `owner` | ForeignKey(User) | Владелец удостоверения |
| `license_number` | CharField | Номер удостоверения |
| `license_type` | CharField | Категория (A, B, C, D) |
| `issue_date` | DateField | Дата выдачи |

### Категории

- **A** - Мотоциклы
- **B** - Легковые автомобили
- **C** - Грузовые автомобили
- **D** - Автобусы

## 🔗 Связи между моделями

```
User ─┬─ owns ──→ Ownership ──→ Car
      │
      └─ has ───→ DriverLicense
```

### Примеры запросов

```python
# Получить все автомобили владельца
owner = User.objects.get(username="ivanov")
ownerships = Ownership.objects.filter(owner=owner, end_date__isnull=True)
cars = [o.car for o in ownerships]

# Получить историю владения автомобилем
car = Car.objects.get(state_number="А123БВ777")
history = Ownership.objects.filter(car=car).order_by('start_date')

# Получить удостоверения владельца
licenses = DriverLicense.objects.filter(owner=owner)
```

## 💾 Миграции

```bash
python manage.py makemigrations
python manage.py migrate
```

## 📊 Примеры данных

```python
# Создание владельца
owner = User.objects.create_user(
    username='ivanov',
    email='ivanov@example.com',
    password='password123',
    first_name='Иван',
    last_name='Иванов',
    passport_number='4509 123456',
    home_address='г. Москва, ул. Ленина, д. 1',
    nationality='Русский',
    birth_date='1990-01-01'
)

# Создание автомобиля
car = Car.objects.create(
    brand='Toyota',
    model='Camry',
    color='Черный',
    state_number='А123БВ777'
)

# Создание владения
ownership = Ownership.objects.create(
    owner=owner,
    car=car,
    start_date='2023-01-01'
)

# Создание удостоверения
license = DriverLicense.objects.create(
    owner=owner,
    license_number='77 12 123456',
    license_type='B',
    issue_date='2010-06-15'
)
```

---

!!! tip "Оптимизация"
    Используйте `select_related()` для оптимизации запросов с ForeignKey!
