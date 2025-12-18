from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from hotel_app.models import *
from datetime import date

User = get_user_model()


class Command(BaseCommand):
    help = 'Заполнение базы данных тестовыми данными для гостиницы'

    def handle(self, *args, **options):
        self.stdout.write('🔄 Начинаем заполнение тестовыми данными...')

        # Очищаем существующие данные в правильном порядке (чтобы избежать ProtectedError)
        self.stdout.write('Очищаем существующие данные...')

        # 1. Сначала удаляем объекты, которые ссылаются на другие модели
        Stay.objects.all().delete()
        CleaningSchedule.objects.all().delete()
        StaffService.objects.all().delete()
        Staff.objects.all().delete()
        HotelService.objects.all().delete()

        # 2. Затем удаляем основные модели
        Room.objects.all().delete()
        Client.objects.all().delete()
        RoomType.objects.all().delete()

        # 3. НЕ удаляем пользователей - будем использовать get_or_create

        # 1. Создаем типы номеров
        self.stdout.write('Создаем типы номеров...')
        room_types = [
            RoomType(name="Одноместный", capacity=1, price_per_night=2000.00,
                     description="Комфортный одноместный номер"),
            RoomType(name="Двухместный", capacity=2, price_per_night=3500.00,
                     description="Просторный двухместный номер"),
            RoomType(name="Трехместный", capacity=3, price_per_night=4500.00,
                     description="Семейный трехместный номер"),
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
                    is_available=True  # Сначала все комнаты доступны
                ))
        Room.objects.bulk_create(rooms)

        # 3. Создаем или обновляем тестовых пользователей
        self.stdout.write('Создаем/обновляем пользователей...')

        # Используем get_or_create чтобы избежать дубликатов
        admin_user, created = User.objects.get_or_create(
            email='admin@hotel.com',
            defaults={
                'username': 'admin',
                'is_staff': True,
                'is_superuser': True,
                'is_admin': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write('  ✅ Создан админ пользователь')
        else:
            self.stdout.write('  ✅ Использован существующий админ пользователь')

        staff1_user, created = User.objects.get_or_create(
            email='staff1@hotel.com',
            defaults={
                'username': 'staff1',
                'is_hotel_staff': True
            }
        )
        if created:
            staff1_user.set_password('staff123')
            staff1_user.save()
            self.stdout.write('  ✅ Создан staff1 пользователь')
        else:
            self.stdout.write('  ✅ Использован существующий staff1 пользователь')

        staff2_user, created = User.objects.get_or_create(
            email='staff2@hotel.com',
            defaults={
                'username': 'staff2',
                'is_hotel_staff': True
            }
        )
        if created:
            staff2_user.set_password('staff123')
            staff2_user.save()
            self.stdout.write('  ✅ Создан staff2 пользователь')
        else:
            self.stdout.write('  ✅ Использован существующий staff2 пользователь')

        users = [admin_user, staff1_user, staff2_user]

        # 4. Создаем сотрудников
        self.stdout.write('Создаем сотрудников...')

        # Удаляем старых сотрудников перед созданием новых
        Staff.objects.all().delete()

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

        # 6. Создаем услуги гостиницы
        self.stdout.write('Создаем услуги гостиницы...')
        HotelService.objects.all().delete()  # Очищаем старые услуги

        services = [
            HotelService(name="Обслуживание номеров", description="Уборка и обслуживание номеров"),
            HotelService(name="Ресепшен", description="Работа на reception"),
            HotelService(name="Обслуживание мероприятий", description="Организация и проведение мероприятий"),
        ]
        HotelService.objects.bulk_create(services)

        service1 = HotelService.objects.get(name="Обслуживание номеров")
        service2 = HotelService.objects.get(name="Ресепшен")
        service3 = HotelService.objects.get(name="Обслуживание мероприятий")

        # 7. Создаем связи многие-ко-многим
        self.stdout.write('Создаем связи сотрудников и услуг...')
        StaffService.objects.all().delete()  # Очищаем старые связи

        staff_services = [
            StaffService(service=service1, staff=ivanov),
            StaffService(service=service1, staff=smirnova),
            StaffService(service=service2, staff=ivanov),
            StaffService(service=service3, staff=smirnova),
        ]
        StaffService.objects.bulk_create(staff_services)

        # 8. Создаем клиентов
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

        # 9. Создаем проживания
        self.stdout.write('Создаем проживания...')
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
            self.style.SUCCESS('✅ Тестовые данные успешно созданы!')
        )

        # Выводим информацию для тестирования
        self.stdout.write('')
        self.stdout.write('📊 Создано:')
        self.stdout.write(f'  - Типов номеров: {RoomType.objects.count()}')
        self.stdout.write(f'  - Комнат: {Room.objects.count()}')
        self.stdout.write(f'  - Клиентов: {Client.objects.count()}')
        self.stdout.write(f'  - Сотрудников: {Staff.objects.count()}')
        self.stdout.write(f'  - Услуг: {HotelService.objects.count()}')
        self.stdout.write(f'  - Связей услуг: {StaffService.objects.count()}')
        self.stdout.write(f'  - Проживаний: {Stay.objects.count()}')

        self.stdout.write('')
        self.stdout.write('🔑 Тестовые пользователи:')
        self.stdout.write('  Админ: admin@hotel.com / admin123')
        self.stdout.write('  Персонал: staff1@hotel.com / staff123')

        self.stdout.write('')
        self.stdout.write('🔍 ID созданных объектов для тестирования:')
        self.stdout.write(f'  - Сотрудник Иванов ID: {ivanov.id}')
        self.stdout.write(f'  - Сотрудник Смирнова ID: {smirnova.id}')
        self.stdout.write(f'  - Услуга "Обслуживание номеров" ID: {service1.id}')
        self.stdout.write(f'  - Услуга "Ресепшен" ID: {service2.id}')

        self.stdout.write('')
        self.stdout.write('🌐 Ссылки для тестирования связи многие-ко-многим:')
        self.stdout.write(f'  - Сотрудник с услугами: http://127.0.0.1:8000/api/staff/{ivanov.id}/with_services/')
        self.stdout.write(
            f'  - Услуга с сотрудниками: http://127.0.0.1:8000/api/hotel-services/{service1.id}/with_staff/')
        self.stdout.write(f'  - Все связи: http://127.0.0.1:8000/api/staff-services/')