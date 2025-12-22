## 1. Цель работы
Разработать информационную систему для управления автоспортивными мероприятиями, включающую:

* Кастомную модель пользователя (гонщика).

* Систему регистрации на гонки с проверкой прав доступа (CRUD).

* Постраничную навигацию (пагинацию) и полнотекстовый поиск.

* Интерфейс на базе Bootstrap 5 с адаптивным меню-бургером.

---

## 2. Архитектура БД (Модели)
В проекте реализованы 4 основные модели: `User`, `Race`, `Registration` и `Comment`.

### Листинг модели пользователя (models.py)
```python
class User(AbstractUser):
    RACER_CHOICES = [
        ('A', 'Класс A (Профессионалы)'),
        ('B', 'Класс B (Любители)'),
        ('C', 'Класс C (Новички)'),
    ]
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    experience = models.PositiveIntegerField(default=0)
    racer_class = models.CharField(max_length=10, choices=RACER_CHOICES, default='C')
    bio = models.TextField(max_length=500, blank=True)

```
![models](/img/models.png)

---

## 3. Реализация функционала

### 3.1. Пагинация и Поиск

Реализован поиск по командам внутри страницы гонки и постраничный вывод результатов (по 5 участников).

**Скриншот 1-2: Главная страница со списком гонок и пагинацией** 
![Главная страница](/img/det1.png)
![Главная страница](/img/det2.png)

**Скриншот 3: Поиск по команде в деталях гонки** 
![Поиск](/img/poisk.png)

### 3.2. Регистрация и CRUD

Пользователь может зарегистрироваться, войти в систему (редирект на главную) и управлять своим участием.

### Листинг логики переключения страниц (views.py)

```python
# Обработка страницы с сохранением поиска в пагинации
page_number = self.request.GET.get('page')
try:
    context['participants'] = paginator.page(page_number)
except PageNotAnInteger:
    context['participants'] = paginator.page(1)

```

**Скриншот 3: Форма регистрации нового гонщика** 
![Рега](/img/reg.png)


---

## 4. Интерфейс пользователя

Сайт использует Bootstrap 5. Для мобильных устройств реализовано "бургер-меню".

### Листинг адаптивной навигации (base.html)

```html
<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
    <span class="navbar-toggler-icon"></span>
</button>
<div class="collapse navbar-collapse" id="navbarNav">
    </div>

```

**Скриншот 4: Мобильный вид (Меню-бургер)** 

На компьютерах
![m1](/img/main1.png)

На мобильных устройствах
![m2](/img/main2.png)

---

## 5. Выводы

В ходе работы была настроена среда Docker, реализована сложная логика связей Many-to-Many через модель `Registration`. Система позволяет гибко управлять составом участников и отзывами. Требования Варианта №6 выполнены в полном объеме.
