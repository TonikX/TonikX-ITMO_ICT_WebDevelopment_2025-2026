from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from flights.models import Airline, Flight, Reservation, Review
import random


class Command(BaseCommand):
    help = 'Загружает образцы данных для демонстрации приложения'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Начинаю загрузку образцов данных...'))

        # Создаем авиакомпании
        airlines_data = [
            {'name': 'Аэрофлот', 'code': 'SU'},
            {'name': 'S7 Airlines', 'code': 'S7'},
            {'name': 'Россия', 'code': 'FV'},
            {'name': 'ЮТэйр', 'code': 'UT'},
            {'name': 'Победа', 'code': 'DP'},
        ]

        airlines = []
        for airline_data in airlines_data:
            airline, created = Airline.objects.get_or_create(
                code=airline_data['code'],
                defaults={'name': airline_data['name']}
            )
            airlines.append(airline)
            if created:
                self.stdout.write(f'Создана авиакомпания: {airline.name}')

        # Создаем рейсы
        cities = [
            ('Москва', 'Санкт-Петербург'),
            ('Москва', 'Сочи'),
            ('Санкт-Петербург', 'Екатеринбург'),
            ('Москва', 'Новосибирск'),
            ('Санкт-Петербург', 'Калининград'),
            ('Москва', 'Краснодар'),
            ('Сочи', 'Екатеринбург'),
            ('Новосибирск', 'Владивосток'),
        ]

        flights = []
        for i in range(20):
            airline = random.choice(airlines)
            origin, destination = random.choice(cities)
            
            # Случайное время в ближайшие 30 дней
            departure_time = timezone.now() + timedelta(
                days=random.randint(0, 30),
                hours=random.randint(6, 22),
                minutes=random.choice([0, 15, 30, 45])
            )
            
            flight_duration = timedelta(hours=random.randint(1, 8), minutes=random.choice([0, 30]))
            arrival_time = departure_time + flight_duration
            
            flight = Flight.objects.create(
                flight_number=f'{airline.code}{random.randint(100, 999)}',
                airline=airline,
                departure_time=departure_time,
                arrival_time=arrival_time,
                flight_type=random.choice(['departure', 'arrival']),
                gate_number=f'{random.randint(1, 20)}{random.choice("ABCD")}',
                origin=origin,
                destination=destination,
                capacity=random.choice([100, 150, 200, 250]),
                price=random.randint(5000, 25000)
            )
            flights.append(flight)

        self.stdout.write(f'Создано {len(flights)} рейсов')

        # Создаем тестового пользователя-администратора
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@airline.com',
                'first_name': 'Администратор',
                'last_name': 'Системы',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write('Создан администратор: admin/admin123')

        # Создаем тестовых пользователей
        test_users = []
        for i in range(5):
            user, created = User.objects.get_or_create(
                username=f'user{i+1}',
                defaults={
                    'email': f'user{i+1}@example.com',
                    'first_name': f'Пользователь',
                    'last_name': f'{i+1}',
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                test_users.append(user)

        self.stdout.write(f'Создано {len(test_users)} тестовых пользователей')

        # Создаем некоторые резервирования
        for i in range(15):
            user = random.choice(test_users)
            flight = random.choice(flights)
            
            # Проверяем, нет ли уже резервирования у этого пользователя на этот рейс
            if not Reservation.objects.filter(user=user, flight=flight).exists():
                seat_number = f'{random.randint(1, 30)}{random.choice("ABCDEF")}'
                
                # Проверяем, свободно ли место
                if not Reservation.objects.filter(flight=flight, seat_number=seat_number).exists():
                    reservation = Reservation.objects.create(
                        user=user,
                        flight=flight,
                        seat_number=seat_number,
                        ticket_number=f'T{random.randint(100000, 999999)}'
                    )

        reservations_count = Reservation.objects.count()
        self.stdout.write(f'Создано {reservations_count} резервирований')

        # Создаем отзывы
        review_texts = [
            'Отличный рейс! Все прошло гладко.',
            'Хорошее обслуживание, вовремя прилетели.',
            'Неплохо, но можно было бы и лучше.',
            'Экипаж очень вежливый, полет комфортный.',
            'Задержка была, но в целом нормально.',
            'Превосходное качество обслуживания!',
            'Среднее качество за свою цену.',
            'Рекомендую эту авиакомпанию!',
        ]

        for i in range(10):
            user = random.choice(test_users)
            flight = random.choice(flights)
            
            # Проверяем, нет ли уже отзыва от этого пользователя на этот рейс
            if not Review.objects.filter(user=user, flight=flight).exists():
                Review.objects.create(
                    user=user,
                    flight=flight,
                    text=random.choice(review_texts),
                    rating=random.randint(6, 10)
                )

        reviews_count = Review.objects.count()
        self.stdout.write(f'Создано {reviews_count} отзывов')

        self.stdout.write(
            self.style.SUCCESS('Загрузка образцов данных завершена!')
        )
        self.stdout.write(
            self.style.WARNING('Для входа в админку используйте: admin/admin123')
        )
        self.stdout.write(
            self.style.WARNING('Тестовые пользователи: user1-user5/password123')
        )
