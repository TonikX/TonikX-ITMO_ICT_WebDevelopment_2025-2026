"""
Скрипт для загрузки тестовых данных в базу
Запуск: python load_test_data.py
"""
import os
import django
import sys

# Настройка Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airport_project.settings')
django.setup()

from datetime import datetime, timedelta
from flights.models import User, Flight, Reservation, Review
from django.utils import timezone

print("Начинаем загрузку тестовых данных...")

# Создаем пользователей
users_data = [
    {
        'username': 'ivanov_p',
        'first_name': 'Петр',
        'last_name': 'Иванов',
        'email': 'ivanov@example.com',
        'phone_number': '+7 (999) 123-45-67',
        'passport_number': '4509 123456',
        'password': 'password123'
    },
    {
        'username': 'petrova_m',
        'first_name': 'Мария',
        'last_name': 'Петрова',
        'email': 'petrova@example.com',
        'phone_number': '+7 (999) 234-56-78',
        'passport_number': '4510 234567',
        'password': 'password123'
    },
    {
        'username': 'sidorov_a',
        'first_name': 'Алексей',
        'last_name': 'Сидоров',
        'email': 'sidorov@example.com',
        'phone_number': '+7 (999) 345-67-89',
        'passport_number': '4511 345678',
        'password': 'password123'
    },
]

users = []
for data in users_data:
    password = data.pop('password')
    user = User.objects.create_user(**data)
    user.set_password(password)
    user.save()
    users.append(user)
    print(f"Создан пользователь: {user.username}")

# Создаем рейсы
now = timezone.now()
flights_data = [
    {
        'flight_number': 'SU1234',
        'airline': 'Аэрофлот',
        'departure_city': 'Москва',
        'arrival_city': 'Санкт-Петербург',
        'departure_time': now + timedelta(days=5, hours=10),
        'arrival_time': now + timedelta(days=5, hours=11, minutes=30),
        'flight_type': 'departure',
        'gate_number': 'A12',
        'total_seats': 180,
        'price': 5500
    },
    {
        'flight_number': 'S71001',
        'airline': 'S7 Airlines',
        'departure_city': 'Москва',
        'arrival_city': 'Новосибирск',
        'departure_time': now + timedelta(days=3, hours=14),
        'arrival_time': now + timedelta(days=3, hours=18),
        'flight_type': 'departure',
        'gate_number': 'B5',
        'total_seats': 150,
        'price': 12000
    },
    {
        'flight_number': 'UT405',
        'airline': 'Utair',
        'departure_city': 'Санкт-Петербург',
        'arrival_city': 'Москва',
        'departure_time': now + timedelta(days=2, hours=9),
        'arrival_time': now + timedelta(days=2, hours=10, minutes=30),
        'flight_type': 'arrival',
        'gate_number': 'C3',
        'total_seats': 120,
        'price': 6000
    },
    {
        'flight_number': 'FV5603',
        'airline': 'Россия',
        'departure_city': 'Москва',
        'arrival_city': 'Сочи',
        'departure_time': now + timedelta(days=7, hours=6),
        'arrival_time': now + timedelta(days=7, hours=8, minutes=20),
        'flight_type': 'departure',
        'gate_number': 'D8',
        'total_seats': 200,
        'price': 8500
    },
    {
        'flight_number': 'N4102',
        'airline': 'Nordwind Airlines',
        'departure_city': 'Екатеринбург',
        'arrival_city': 'Москва',
        'departure_time': now + timedelta(days=1, hours=16),
        'arrival_time': now + timedelta(days=1, hours=18),
        'flight_type': 'arrival',
        'gate_number': 'A7',
        'total_seats': 160,
        'price': 9500
    },
]

flights = []
for data in flights_data:
    flight = Flight.objects.create(**data)
    flights.append(flight)
    print(f"Создан рейс: {flight.flight_number} - {flight.departure_city} → {flight.arrival_city}")

# Создаем резервирования
reservations_data = [
    {'user': users[0], 'flight': flights[0], 'status': 'confirmed', 'is_confirmed': True, 'ticket_number': 'T001234', 'seat_number': '12A'},
    {'user': users[1], 'flight': flights[0], 'status': 'confirmed', 'is_confirmed': True, 'ticket_number': 'T001235', 'seat_number': '12B'},
    {'user': users[0], 'flight': flights[1], 'status': 'pending', 'is_confirmed': False},
    {'user': users[2], 'flight': flights[2], 'status': 'confirmed', 'is_confirmed': True, 'ticket_number': 'T002001', 'seat_number': '5C'},
    {'user': users[1], 'flight': flights[3], 'status': 'confirmed', 'is_confirmed': True, 'ticket_number': 'T003015', 'seat_number': '8D'},
    {'user': users[2], 'flight': flights[4], 'status': 'pending', 'is_confirmed': False},
]

for data in reservations_data:
    reservation = Reservation.objects.create(**data)
    print(f"Создано резервирование: {reservation.user.username} → {reservation.flight.flight_number}")

# Создаем отзывы
reviews_data = [
    {
        'user': users[0],
        'flight': flights[0],
        'flight_date': (now - timedelta(days=30)).date(),
        'rating': 9,
        'text': 'Отличный рейс! Вылет и прилет точно по расписанию. Экипаж вежливый и внимательный.'
    },
    {
        'user': users[1],
        'flight': flights[0],
        'flight_date': (now - timedelta(days=25)).date(),
        'rating': 8,
        'text': 'Хороший сервис, удобные кресла. Единственный минус - небольшая задержка при посадке.'
    },
    {
        'user': users[2],
        'flight': flights[2],
        'flight_date': (now - timedelta(days=20)).date(),
        'rating': 7,
        'text': 'Нормальный рейс, но питание могло бы быть лучше.'
    },
    {
        'user': users[1],
        'flight': flights[3],
        'flight_date': (now - timedelta(days=15)).date(),
        'rating': 10,
        'text': 'Превосходно! Комфортный полет, отличный сервис. Рекомендую!'
    },
]

for data in reviews_data:
    review = Review.objects.create(**data)
    print(f"Создан отзыв: {review.user.username} → {review.flight.flight_number} ({review.rating}/10)")

print("\n" + "="*60)
print("ТЕСТОВЫЕ ДАННЫЕ УСПЕШНО ЗАГРУЖЕНЫ!")
print("="*60)
print(f"\nСтатистика:")
print(f"  Пользователей: {User.objects.count()}")
print(f"  Рейсов: {Flight.objects.count()}")
print(f"  Резервирований: {Reservation.objects.count()}")
print(f"  Отзывов: {Review.objects.count()}")
print(f"\nДанные для входа:")
print(f"  Админ: admin / admin")
print(f"  Пользователи: ivanov_p / password123, petrova_m / password123, sidorov_a / password123")
print(f"\nЗапустите сервер: python manage.py runserver")



