"""
Management команда для загрузки тестовых данных в БД
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from api.models import Room, Guest, Staff, CleaningSchedule
import random
from datetime import timedelta

fake = Faker('ru_RU')


class Command(BaseCommand):
    help = 'Загрузка тестовых данных в базу данных гостиницы'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Очистить существующие данные перед загрузкой',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Очистка существующих данных...')
            CleaningSchedule.objects.all().delete()
            Guest.objects.all().delete()
            Staff.objects.all().delete()
            Room.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Данные очищены'))

        self.stdout.write('Создание номеров...')
        rooms = self.create_rooms()
        self.stdout.write(self.style.SUCCESS(f'Создано {len(rooms)} номеров'))

        self.stdout.write('Создание служащих...')
        staff = self.create_staff()
        self.stdout.write(self.style.SUCCESS(f'Создано {len(staff)} служащих'))

        self.stdout.write('Создание расписания уборки...')
        schedules = self.create_cleaning_schedules(staff, rooms)
        self.stdout.write(self.style.SUCCESS(f'Создано {len(schedules)} записей расписания'))

        self.stdout.write('Создание гостей...')
        guests = self.create_guests(rooms)
        self.stdout.write(self.style.SUCCESS(f'Создано {len(guests)} гостей'))

        self.stdout.write(self.style.SUCCESS('Все данные успешно загружены!'))
        self.print_summary(rooms, staff, guests, schedules)

    def create_rooms(self):
        """Создание номеров"""
        rooms = []
        room_types = ['single', 'double', 'triple']
        prices = {'single': 2500, 'double': 3500, 'triple': 4500}
        
        # Гостиница на 5 этажах, по 10 номеров на этаже
        room_number = 100
        for floor in range(1, 6):
            for room_on_floor in range(1, 11):
                room_number = floor * 100 + room_on_floor
                room_type = random.choice(room_types)
                
                room = Room.objects.create(
                    number=str(room_number),
                    room_type=room_type,
                    floor=floor,
                    phone=f'+7 (495) {random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}',
                    price_per_day=prices[room_type]
                )
                rooms.append(room)
        
        return rooms

    def create_staff(self):
        """Создание служащих"""
        staff_list = []
        
        # Создаем 15 служащих
        for i in range(15):
            hire_date = fake.date_between(start_date='-3y', end_date='-1m')
            
            # 80% служащих активны
            is_active = random.random() > 0.2
            fire_date = None
            
            if not is_active:
                fire_date = fake.date_between(start_date=hire_date, end_date='today')
            
            staff_member = Staff.objects.create(
                last_name=fake.last_name(),
                first_name=fake.first_name(),
                middle_name=fake.middle_name(),
                is_active=is_active,
                hire_date=hire_date,
                fire_date=fire_date
            )
            staff_list.append(staff_member)
        
        return staff_list

    def create_cleaning_schedules(self, staff_list, rooms):
        """Создание расписания уборки"""
        schedules = []
        active_staff = [s for s in staff_list if s.is_active]
        
        # Получаем уникальные этажи
        floors = sorted(set(room.floor for room in rooms))
        
        # Для каждого этажа назначаем служащих на разные дни недели
        for floor in floors:
            # Выбираем 3-5 служащих для этого этажа
            staff_for_floor = random.sample(active_staff, min(random.randint(3, 5), len(active_staff)))
            
            for staff_member in staff_for_floor:
                # Назначаем 2-3 дня недели
                weekdays = random.sample(range(1, 8), random.randint(2, 3))
                
                for weekday in weekdays:
                    try:
                        schedule = CleaningSchedule.objects.create(
                            staff=staff_member,
                            floor=floor,
                            weekday=weekday
                        )
                        schedules.append(schedule)
                    except:
                        # Если уже есть такая запись, пропускаем
                        pass
        
        return schedules

    def create_guests(self, rooms):
        """Создание гостей"""
        guests = []
        cities = [
            'Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург',
            'Казань', 'Нижний Новгород', 'Челябинск', 'Самара',
            'Омск', 'Ростов-на-Дону', 'Уфа', 'Красноярск',
            'Воронеж', 'Пермь', 'Волгоград', 'Краснодар'
        ]
        
        today = timezone.now().date()
        
        # Создаем историю за последние 6 месяцев
        for i in range(100):
            # Генерируем уникальный номер паспорта
            passport_number = f"{random.randint(1000, 9999)} {random.randint(100000, 999999)}"
            
            # Проверяем, что такого паспорта еще нет
            while Guest.objects.filter(passport_number=passport_number).exists():
                passport_number = f"{random.randint(1000, 9999)} {random.randint(100000, 999999)}"
            
            # Дата заселения в прошлом
            check_in_date = fake.date_between(start_date='-6m', end_date='today')
            
            # 70% гостей уже выселились
            check_out_date = None
            if random.random() > 0.3:
                # Продолжительность проживания от 1 до 14 дней
                days_stayed = random.randint(1, 14)
                check_out_date = check_in_date + timedelta(days=days_stayed)
                
                # Не даем дату выселения в будущем
                if check_out_date > today:
                    check_out_date = today
            
            # Выбираем случайный номер
            room = random.choice(rooms)
            
            # Проверяем, что номер свободен в этот период
            overlapping_guests = Guest.objects.filter(
                room=room,
                check_in_date__lte=check_out_date if check_out_date else check_in_date,
            ).filter(
                models.Q(check_out_date__isnull=True) | 
                models.Q(check_out_date__gte=check_in_date)
            )
            
            # Если номер занят, ищем другой
            attempts = 0
            while overlapping_guests.exists() and attempts < 20:
                room = random.choice(rooms)
                overlapping_guests = Guest.objects.filter(
                    room=room,
                    check_in_date__lte=check_out_date if check_out_date else check_in_date,
                ).filter(
                    models.Q(check_out_date__isnull=True) | 
                    models.Q(check_out_date__gte=check_in_date)
                )
                attempts += 1
            
            if attempts >= 20:
                continue  # Пропускаем, если не нашли свободный номер
            
            guest = Guest.objects.create(
                passport_number=passport_number,
                last_name=fake.last_name(),
                first_name=fake.first_name(),
                middle_name=fake.middle_name(),
                city=random.choice(cities),
                room=room,
                check_in_date=check_in_date,
                check_out_date=check_out_date
            )
            guests.append(guest)
        
        return guests

    def print_summary(self, rooms, staff, guests, schedules):
        """Вывод сводки по загруженным данным"""
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(self.style.SUCCESS('СВОДКА ПО ЗАГРУЖЕННЫМ ДАННЫМ'))
        self.stdout.write('=' * 50)
        
        self.stdout.write(f'\nВсего номеров: {len(rooms)}')
        for room_type in ['single', 'double', 'triple']:
            count = sum(1 for r in rooms if r.room_type == room_type)
            self.stdout.write(f'  - {Room.ROOM_TYPES[["single", "double", "triple"].index(room_type)][1]}: {count}')
        
        self.stdout.write(f'\nВсего служащих: {len(staff)}')
        active_count = sum(1 for s in staff if s.is_active)
        self.stdout.write(f'  - Активных: {active_count}')
        self.stdout.write(f'  - Уволенных: {len(staff) - active_count}')
        
        self.stdout.write(f'\nВсего гостей: {len(guests)}')
        current_guests = sum(1 for g in guests if g.is_current)
        self.stdout.write(f'  - Проживающих сейчас: {current_guests}')
        self.stdout.write(f'  - Выселившихся: {len(guests) - current_guests}')
        
        self.stdout.write(f'\nЗаписей в расписании уборки: {len(schedules)}')
        
        self.stdout.write('\n' + '=' * 50 + '\n')


from django.db import models
