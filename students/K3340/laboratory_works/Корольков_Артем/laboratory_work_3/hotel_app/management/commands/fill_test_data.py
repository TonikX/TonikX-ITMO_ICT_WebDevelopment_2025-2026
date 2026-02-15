from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from hotel_app.models import *

User = get_user_model()


class Command(BaseCommand):
    help = 'Заполнение базы данных тестовыми данными для гостиницы'

    def handle(self, *args, **options):
        self.stdout.write('🔄 Начинаем заполнение тестовыми данными...')

        # Очищаем существующие данные (осторожно!)
        RoomType.objects.all().delete()
        Room.objects.all().delete()
        Client.objects.all().delete()
        Staff.objects.all().delete()
        CleaningSchedule.objects.all().delete()
        Stay.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        # 1. Создаем типы номеров
        self.stdout.write('Создаем типы номеров...')
        room_types = [
            RoomType(name="Одноместный", capacity=1, price_per_night=2000.00,
                     description="Комфортный одноместный номер"),
            RoomType(name="Двухместный", capacity=2, price_per_night=3500.00,
                     description="Просторный двухместный номер"),
            RoomType(name="Трехместный", capacity=3, price_per_night=4500.00, description="Семейный трехместный номер"),
        ]
        RoomType.objects.bulk_create(room_types)

        single = RoomType.objects.get(name="Одноместный")
        double = RoomType.objects.get(name="Двухместный")
        triple = RoomType.objects.get(name="Трехместный")

        # 2. Создаем комнаты
        self.stdout.write('Создаем комнаты...')
        rooms = []
        for floor in range(1, 4):
            for room_num in range(1, 11):
                room_number = f"{floor}{room_num:02d}"
                # Распределяем типы номеров по этажам
                if floor == 1:
                    room_type = single
                elif floor == 2:
                    room_type = double
                else:
                    room_type = triple

                rooms.append(Room(
                    room_number=room_number,
                    floor=floor,
                    room_type=room_type,
                    has_phone=True,
                    is_available=room_num % 3 != 0  # Каждая 3-я комната занята
                ))
        Room.objects.bulk_create(rooms)

        # 3. Создаем тестовых пользователей
        self.stdout.write('Создаем пользователей...')
        users = [
            User.objects.create_user(
                email='admin@hotel.com',
                username='admin',
                password='admin123',
                is_admin=True
            ),
            User.objects.create_user(
                email='staff1@hotel.com',
                username='staff1',
                password='staff123',
                is_hotel_staff=True
            ),
            User.objects.create_user(
                email='staff2@hotel.com',
                username='staff2',
                password='staff123',
                is_hotel_staff=True
            ),
        ]

        # 4. Создаем сотрудников
        self.stdout.write('Создаем сотрудников...')
        staff_members = [
            Staff(
                user=users[1],
                last_name="Иванов",
                first_name="Петр",
                middle_name="Сергеевич",
                is_active=True
            ),
            Staff(
                user=users[2],
                last_name="Смирнова",
                first_name="Ольга",
                middle_name="Владимировна",
                is_active=True
            ),
        ]
        Staff.objects.bulk_create(staff_members)

        ivanov = Staff.objects.get(last_name="Иванов")
        smirnova = Staff.objects.get(last_name="Смирнова")

        # 5. Создаем расписание уборки
        self.stdout.write('Создаем расписание уборки...')
        cleaning_schedules = [
            CleaningSchedule(staff=ivanov, floor=1, day_of_week='MON'),
            CleaningSchedule(staff=ivanov, floor=1, day_of_week='WED'),
            CleaningSchedule(staff=ivanov, floor=1, day_of_week='FRI'),
            CleaningSchedule(staff=smirnova, floor=2, day_of_week='TUE'),
            CleaningSchedule(staff=smirnova, floor=2, day_of_week='THU'),
            CleaningSchedule(staff=smirnova, floor=3, day_of_week='MON'),
            CleaningSchedule(staff=ivanov, floor=3, day_of_week='SAT'),
        ]
        CleaningSchedule.objects.bulk_create(cleaning_schedules)

        # 6. Создаем клиентов
        self.stdout.write('Создаем клиентов...')
        clients = [
            Client(
                passport_number="4501123456",
                last_name="Петров",
                first_name="Алексей",
                middle_name="Игоревич",
                city="Москва"
            ),
            Client(
                passport_number="4501654321",
                last_name="Сидорова",
                first_name="Мария",
                middle_name="Петровна",
                city="Санкт-Петербург"
            ),
            Client(
                passport_number="4501789456",
                last_name="Козлов",
                first_name="Дмитрий",
                middle_name="Александрович",
                city="Москва"
            ),
            Client(
                passport_number="4501321654",
                last_name="Николаева",
                first_name="Анна",
                middle_name="Сергеевна",
                city="Казань"
            ),
        ]
        Client.objects.bulk_create(clients)

        petrov = Client.objects.get(last_name="Петров")
        sidorova = Client.objects.get(last_name="Сидорова")
        kozlov = Client.objects.get(last_name="Козлов")
        nikolaeva = Client.objects.get(last_name="Николаева")

        # 7. Создаем проживания
        self.stdout.write('Создаем проживания...')
        from datetime import date, timedelta

        stays = [
            Stay(
                client=petrov,
                room=Room.objects.get(room_number="101"),
                check_in_date=date(2024, 1, 10),
                check_out_date=date(2024, 1, 15)
            ),
            Stay(
                client=sidorova,
                room=Room.objects.get(room_number="201"),
                check_in_date=date(2024, 1, 12),
                check_out_date=date(2024, 1, 18)
            ),
            Stay(
                client=kozlov,
                room=Room.objects.get(room_number="102"),
                check_in_date=date(2024, 1, 5),
                check_out_date=None  # Текущее проживание
            ),
            Stay(
                client=nikolaeva,
                room=Room.objects.get(room_number="301"),
                check_in_date=date(2024, 1, 8),
                check_out_date=date(2024, 1, 14)
            ),
        ]
        for stay in stays:
            stay.save()

        # Обновляем доступность комнат
        for stay in Stay.objects.filter(check_out_date__isnull=True):
            stay.room.is_available = False
            stay.room.save()

        self.stdout.write(
            self.style.SUCCESS('Тестовые данные успешно созданы!')
        )
        self.stdout.write('')
        self.stdout.write('Создано:')
        self.stdout.write(f'  - Типов номеров: {RoomType.objects.count()}')
        self.stdout.write(f'  - Комнат: {Room.objects.count()}')
        self.stdout.write(f'  - Клиентов: {Client.objects.count()}')
        self.stdout.write(f'  - Сотрудников: {Staff.objects.count()}')
        self.stdout.write(f'  - Проживаний: {Stay.objects.count()}')
        self.stdout.write('')
        self.stdout.write('Тестовые пользователи:')
        self.stdout.write('  Админ: admin@hotel.com / admin123')
        self.stdout.write('  Персонал: staff1@hotel.com / staff123')