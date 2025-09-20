# Отчет по лабораторной работе №2

## Цель:

Овладеть практическими навыками и умениями реализации web-сервисов
средствами Django 2.2.

## Задание:

Реализовать сайт используя фреймворк Django 3 и СУБД PostgreSQL, в
соответствии с вариантом задания лабораторной работы.

## Текст задания:

**Список туров туристической фирмы**

Хранится информация о названии тура, турагенстве, описании тура, периоде
проведения тура, условиях оплаты.
Необходимо реализовать следующий функционал:
    * Регистрация новых пользователей.
    * Просмотр и резервирование туров. Пользователь должен иметь возможность
    редактирования и удаления своих резервирований.
    * Написание отзывов к турам. При добавлении комментариев, должны
    сохраняться даты тура, текст комментария, рейтинг (1-10), информация о
    комментаторе.
    * Администратор должен иметь возможность подтвердить резервирование
    тура средствами Django-admin.
    * В клиентской части должна формироваться таблица, отображающая все
    проданные туры по странам.

## Выполнение

#### 1. Создание проекта

Django проект был создан под названием 'travelCompany', а внутри два приложения: users для работы с пользователями и 
main для работы со всей остальной логикой приложения.

#### 2. Создание моделей

В приложении main были созданы три модели: Tour (информация о туре), Reservation (информация о бронировании), Review 
(информация об отзывах)

```python
from django.conf import settings
from django.db import models

class Tour(models.Model):
    """Класс тура"""

    name = models.CharField(max_length=200, verbose_name="Название тура")
    agency = models.CharField(max_length=150, verbose_name="Турагенство")
    description = models.TextField(verbose_name="Описание тура")
    country = models.CharField(max_length=50, verbose_name="Страна")
    start_date = models.DateField(verbose_name="Дата начала тура")
    end_date = models.DateField(verbose_name="Дата окончания тура")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость тура")

    def __str__(self):
        return self.name

class Reservation(models.Model):
    """Класс для резервирования тура пользователем"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations', verbose_name="Пользователь")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reservations', verbose_name="Тур")
    reserved_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата бронирования")
    status = models.BooleanField(default=False, verbose_name="Подтверждено администратором")

    def __str__(self):
        return f"{self.user} - {self.tour}"

class Review(models.Model):
    """Класс для отзывов"""

    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reviews', verbose_name="Тур")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews', verbose_name="Пользователь")
    tour_date = models.DateField(verbose_name="Дата тура")
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.PositiveSmallIntegerField(verbose_name="Оценка тура (1-10)")

    def __str__(self):
        return f"{self.tour} - {self.user} ({self.rating})"
```

В приложении users была создана модель Users, расширяющая базовый класс пользователя.

```python
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    reserved_tours = models.ManyToManyField('main.Tour', through='main.Reservation')

    def __str__(self):
        return self.username
```

После создания моделей были созданы миграции и создан супер пользователь.

#### 3. Написание логики регистрации, авторизации, редактирования и выхода для пользователя

