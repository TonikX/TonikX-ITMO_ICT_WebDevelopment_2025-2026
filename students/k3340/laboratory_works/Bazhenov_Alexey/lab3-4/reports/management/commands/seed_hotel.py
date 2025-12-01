from datetime import date
from decimal import Decimal

from django.core.management.base import BaseCommand

from clients.models import Client
from employees.models import CleaningAssignment, Employee
from rooms.models import Room
from stays.models import Stay


class Command(BaseCommand):
    help = 'Наполняет базу демонстрационными данными гостиницы.'

    def handle(self, *args, **options):
        self.stdout.write('Создаю номера...')
        rooms = [
            {'number': 101, 'floor': 1, 'room_type': Room.RoomType.SINGLE, 'daily_rate': Decimal('3500'), 'phone_number': '1001'},
            {'number': 102, 'floor': 1, 'room_type': Room.RoomType.DOUBLE, 'daily_rate': Decimal('5200'), 'phone_number': '1002'},
            {'number': 201, 'floor': 2, 'room_type': Room.RoomType.TRIPLE, 'daily_rate': Decimal('7200'), 'phone_number': '2001'},
            {'number': 202, 'floor': 2, 'room_type': Room.RoomType.DOUBLE, 'daily_rate': Decimal('5400'), 'phone_number': '2002'},
            {'number': 301, 'floor': 3, 'room_type': Room.RoomType.SINGLE, 'daily_rate': Decimal('3600'), 'phone_number': '3001'},
        ]
        room_objects = []
        for payload in rooms:
            room, _ = Room.objects.get_or_create(
                number=payload['number'],
                defaults={
                    'floor': payload['floor'],
                    'room_type': payload['room_type'],
                    'daily_rate': payload['daily_rate'],
                    'phone_number': payload['phone_number'],
                    'capacity': Room.ROOM_TYPE_CAPACITY[payload['room_type']],
                },
            )
            room_objects.append(room)

        self.stdout.write('Создаю клиентов...')
        clients_data = [
            {'passport_number': '4010 123456', 'last_name': 'Иванов', 'first_name': 'Алексей', 'middle_name': 'Петрович', 'city': 'Москва', 'phone': '+7 900 100-00-01'},
            {'passport_number': '4011 654321', 'last_name': 'Петрова', 'first_name': 'Мария', 'middle_name': 'Игоревна', 'city': 'Санкт-Петербург', 'phone': '+7 900 100-00-02'},
            {'passport_number': '4012 777777', 'last_name': 'Смирнов', 'first_name': 'Дмитрий', 'middle_name': 'Олегович', 'city': 'Казань', 'phone': '+7 900 100-00-03'},
            {'passport_number': '4013 888888', 'last_name': 'Кузнецова', 'first_name': 'Елена', 'middle_name': 'Андреевна', 'city': 'Новосибирск', 'phone': '+7 900 100-00-04'},
        ]
        client_objects = []
        for payload in clients_data:
            client, _ = Client.objects.get_or_create(passport_number=payload['passport_number'], defaults=payload)
            client_objects.append(client)

        self.stdout.write('Создаю сотрудников и расписания...')
        employees_data = [
            {
                'name': {'last_name': 'Сидоров', 'first_name': 'Илья', 'middle_name': 'Викторович'},
                'assignments': [(1, 'mon'), (1, 'wed'), (2, 'fri')],
            },
            {
                'name': {'last_name': 'Алексеева', 'first_name': 'Наталья', 'middle_name': 'Сергеевна'},
                'assignments': [(2, 'tue'), (3, 'thu'), (3, 'sat')],
            },
        ]
        for item in employees_data:
            employee, _ = Employee.objects.get_or_create(**item['name'])
            employee.assignments.all().delete()
            CleaningAssignment.objects.bulk_create(
                [
                    CleaningAssignment(employee=employee, floor=floor, weekday=weekday)
                    for floor, weekday in item['assignments']
                ]
            )

        self.stdout.write('Создаю проживание...')
        stay_presets = [
            {
                'client': client_objects[0],
                'room': Room.objects.get(number=101),
                'check_in': date(2025, 1, 10),
                'check_out': date(2025, 1, 15),
            },
            {
                'client': client_objects[1],
                'room': Room.objects.get(number=102),
                'check_in': date(2025, 2, 3),
                'check_out': date(2025, 2, 10),
            },
            {
                'client': client_objects[2],
                'room': Room.objects.get(number=202),
                'check_in': date(2025, 3, 1),
                'check_out': None,
            },
            {
                'client': client_objects[3],
                'room': Room.objects.get(number=201),
                'check_in': date(2025, 3, 5),
                'check_out': None,
            },
        ]
        for preset in stay_presets:
            stay, created = Stay.objects.get_or_create(
                client=preset['client'],
                room=preset['room'],
                check_in=preset['check_in'],
                defaults={'status': Stay.Status.ACTIVE},
            )
            if created and preset['check_out']:
                stay.close(preset['check_out'])
                stay.save()

        self.stdout.write(self.style.SUCCESS('База успешно заполнена демонстрационными данными.'))

