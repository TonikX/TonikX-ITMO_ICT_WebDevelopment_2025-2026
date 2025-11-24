#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.agency.models import Client, Employee, ServiceCategory, Service, Order, PaymentOrder
from datetime import date, timedelta
from decimal import Decimal
import random

# Очистка
PaymentOrder.objects.all().delete()
Order.objects.all().delete()
Service.objects.all().delete()
ServiceCategory.objects.all().delete()
Employee.objects.all().delete()
Client.objects.all().delete()

# Пользователь
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@test.ru', 'admin')
    print('Создан пользователь: admin / admin')

# Клиенты
clients = [
    Client.objects.create(name='ООО "Альфа"', contact_person='Иванов Иван', phone='+7-900-111-11-11', email='ivanov@alfa.ru'),
    Client.objects.create(name='ЗАО "Бета"', contact_person='Петров Петр', phone='+7-900-222-22-22', email='petrov@beta.ru'),
    Client.objects.create(name='ИП Сидоров', contact_person='Сидоров Сидор', phone='+7-900-333-33-33', email='sidorov@mail.ru'),
    Client.objects.create(name='ООО "Гамма"', contact_person='Козлов Андрей', phone='+7-900-444-44-44', email='kozlov@gamma.ru'),
    Client.objects.create(name='АО "Дельта"', contact_person='Смирнова Анна', phone='+7-900-555-55-55', email='smirnova@delta.ru'),
]
print(f'Создано клиентов: {len(clients)}')

# Сотрудники
employees = [
    Employee.objects.create(first_name='Алексей', last_name='Кузнецов', phone='+7-901-111-11-11', email='kuznetsov@luch.ru', position='Дизайнер'),
    Employee.objects.create(first_name='Мария', last_name='Новикова', phone='+7-901-222-22-22', email='novikova@luch.ru', position='Менеджер'),
    Employee.objects.create(first_name='Дмитрий', last_name='Морозов', phone='+7-901-333-33-33', email='morozov@luch.ru', position='Копирайтер'),
    Employee.objects.create(first_name='Елена', last_name='Волкова', phone='+7-901-444-44-44', email='volkova@luch.ru', position='Дизайнер'),
]
print(f'Создано сотрудников: {len(employees)}')

# Категории услуг
categories = [
    ServiceCategory.objects.create(name='Наружная реклама'),
    ServiceCategory.objects.create(name='Полиграфия'),
    ServiceCategory.objects.create(name='Интернет-реклама'),
    ServiceCategory.objects.create(name='Видеореклама'),
]
print(f'Создано категорий: {len(categories)}')

# Услуги
services = [
    Service.objects.create(category=categories[0], name='Баннер 3x6м', price=Decimal('15000'), unit='шт', materials='Винил, металлоконструкция'),
    Service.objects.create(category=categories[0], name='Вывеска световая', price=Decimal('25000'), unit='шт', materials='Акрил, LED'),
    Service.objects.create(category=categories[1], name='Буклет А4', price=Decimal('500'), unit='100 шт', materials='Бумага мелованная'),
    Service.objects.create(category=categories[1], name='Визитки', price=Decimal('800'), unit='1000 шт', materials='Картон 300г'),
    Service.objects.create(category=categories[2], name='Контекстная реклама', price=Decimal('10000'), unit='месяц', materials=''),
    Service.objects.create(category=categories[2], name='Таргетированная реклама', price=Decimal('12000'), unit='месяц', materials=''),
    Service.objects.create(category=categories[3], name='Видеоролик 30 сек', price=Decimal('50000'), unit='шт', materials=''),
    Service.objects.create(category=categories[3], name='Анимация логотипа', price=Decimal('8000'), unit='шт', materials=''),
]
print(f'Создано услуг: {len(services)}')

# Заявки
orders = []
statuses = ['new', 'in_progress', 'completed']
for i in range(15):
    order = Order.objects.create(
        client=random.choice(clients),
        service=random.choice(services),
        executor=random.choice(employees),
        quantity=random.randint(1, 10),
        total_cost=Decimal(random.randint(5000, 100000)),
        status=random.choice(statuses),
    )
    orders.append(order)
print(f'Создано заявок: {len(orders)}')

# Платежные поручения
payments = []
for order in orders:
    is_paid = order.status == 'completed'
    payment = PaymentOrder.objects.create(
        order=order,
        is_paid=is_paid,
        payment_date=date.today() - timedelta(days=random.randint(1, 30)) if is_paid else None,
    )
    payments.append(payment)
print(f'Создано платежных поручений: {len(payments)}')

print('\nГотово! Данные загружены.')
