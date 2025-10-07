from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from flights.models import Flight
from datetime import timedelta
from django.utils import timezone


class Command(BaseCommand):
    help = 'Populate database with sample flight data'

    def handle(self, *args, **options):
        # Создаем тестовые рейсы
        flights_data = [
            {
                'flight_number': 'SU123',
                'airline': 'Аэрофлот',
                'departure_time': timezone.now() + timedelta(hours=2),
                'arrival_time': timezone.now() + timedelta(hours=5),
                'flight_type': 'departure',
                'gate_number': 'A12',
                'total_seats': 150
            },
            {
                'flight_number': 'S7456',
                'airline': 'S7 Airlines',
                'departure_time': timezone.now() + timedelta(hours=4),
                'arrival_time': timezone.now() + timedelta(hours=8),
                'flight_type': 'departure',
                'gate_number': 'B3',
                'total_seats': 180
            },
            {
                'flight_number': 'BA789',
                'airline': 'British Airways',
                'departure_time': timezone.now() + timedelta(hours=1),
                'arrival_time': timezone.now() + timedelta(hours=6),
                'flight_type': 'arrival',
                'gate_number': 'C5',
                'total_seats': 200
            },
            {
                'flight_number': 'LH321',
                'airline': 'Lufthansa',
                'departure_time': timezone.now() + timedelta(hours=3),
                'arrival_time': timezone.now() + timedelta(hours=7),
                'flight_type': 'arrival',
                'gate_number': 'D8',
                'total_seats': 160
            },
            {
                'flight_number': 'AF654',
                'airline': 'Air France',
                'departure_time': timezone.now() + timedelta(hours=5),
                'arrival_time': timezone.now() + timedelta(hours=10),
                'flight_type': 'departure',
                'gate_number': 'E2',
                'total_seats': 170
            }
        ]

        for data in flights_data:
            flight, created = Flight.objects.get_or_create(
                flight_number=data['flight_number'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Создан рейс: {flight.flight_number}'))
            else:
                self.stdout.write(self.style.WARNING(f'Рейс уже существует: {flight.flight_number}'))

        self.stdout.write(self.style.SUCCESS('Данные успешно загружены!'))
