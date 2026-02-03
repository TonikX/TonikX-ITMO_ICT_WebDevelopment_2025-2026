from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from hotels.models import Hotel, RoomType, Reservation, Review
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Загружает тестовые данные (отели, номера, резервирования, отзывы)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Очистить существующие данные перед загрузкой',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Очистка существующих данных...')
            Review.objects.all().delete()
            Reservation.objects.all().delete()
            RoomType.objects.all().delete()
            Hotel.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS('Данные очищены'))

        # Создаем тестовых пользователей
        self.stdout.write('Создание пользователей...')
        users = []
        test_users_data = [
            {'username': 'ivan_petrov', 'email': 'ivan@example.com', 'first_name': 'Иван', 'last_name': 'Петров'},
            {'username': 'maria_ivanova', 'email': 'maria@example.com', 'first_name': 'Мария', 'last_name': 'Иванова'},
            {'username': 'alex_sidorov', 'email': 'alex@example.com', 'first_name': 'Алексей', 'last_name': 'Сидоров'},
        ]
        
        for user_data in test_users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                }
            )
            if created:
                user.set_password('test12345')
                user.save()
            users.append(user)
            self.stdout.write(f'  ✓ Пользователь: {user.username}')

        # Создаем отели
        self.stdout.write('Создание отелей...')
        hotels_data = [
            {
                'name': 'Гранд Отель Москва',
                'owner': 'ООО "Гранд Отель"',
                'address': 'г. Москва, Тверская ул., д. 12',
                'description': 'Пятизвездочный отель в самом центре Москвы. Роскошные номера с видом на Кремль, ресторан высокой кухни, спа-центр с бассейном и фитнес-залом. Идеальное место для деловых поездок и романтических выходных.'
            },
            {
                'name': 'Уютный Дворик',
                'owner': 'ИП Иванов И.И.',
                'address': 'г. Санкт-Петербург, Невский пр., д. 45',
                'description': 'Небольшой семейный отель с домашней атмосферой в историческом центре Санкт-Петербурга. Уютные номера, домашняя кухня, дружелюбный персонал. Отличное соотношение цена-качество.'
            },
            {
                'name': 'Морской Бриз',
                'owner': 'ООО "Курорт Сервис"',
                'address': 'г. Сочи, ул. Приморская, д. 8',
                'description': 'Современный отель на берегу Черного моря. Номера с балконами и видом на море, собственный пляж, ресторан с морской кухней, детская площадка. Идеально для семейного отдыха.'
            },
            {
                'name': 'Бизнес Центр',
                'owner': 'ООО "Деловой Отель"',
                'address': 'г. Екатеринбург, ул. Ленина, д. 50',
                'description': 'Отель для деловых людей в центре Екатеринбурга. Современные номера, конференц-залы, бизнес-центр, фитнес. Удобное расположение рядом с деловым центром города.'
            },
        ]

        hotels = []
        for hotel_data in hotels_data:
            hotel, created = Hotel.objects.get_or_create(
                name=hotel_data['name'],
                defaults=hotel_data
            )
            hotels.append(hotel)
            self.stdout.write(f'  ✓ Отель: {hotel.name}')

        # Создаем типы номеров
        self.stdout.write('Создание типов номеров...')
        room_types_data = [
            # Гранд Отель Москва
            {
                'hotel': hotels[0],
                'name': 'Стандартный одноместный',
                'description': 'Уютный номер для одного человека с видом во двор',
                'price': 3500.00,
                'capacity': 1,
                'amenities': ['wifi', 'tv', 'minibar', 'bathroom'],
                'available_count': 5
            },
            {
                'hotel': hotels[0],
                'name': 'Стандартный двухместный',
                'description': 'Комфортный номер для двух человек с видом на город',
                'price': 5000.00,
                'capacity': 2,
                'amenities': ['wifi', 'tv', 'minibar', 'conditioner', 'bathroom', 'balcony'],
                'available_count': 10
            },
            {
                'hotel': hotels[0],
                'name': 'Люкс',
                'description': 'Роскошный номер с панорамным видом на Кремль, гостиная и спальня',
                'price': 12000.00,
                'capacity': 4,
                'amenities': ['wifi', 'tv', 'minibar', 'conditioner', 'safe', 'bathroom', 'balcony'],
                'available_count': 3
            },
            {
                'hotel': hotels[0],
                'name': 'Президентский люкс',
                'description': 'Самый роскошный номер отеля с отдельной гостиной, столовой и кабинетом',
                'price': 25000.00,
                'capacity': 6,
                'amenities': ['wifi', 'tv', 'minibar', 'conditioner', 'safe', 'bathroom', 'balcony'],
                'available_count': 1
            },
            # Уютный Дворик
            {
                'hotel': hotels[1],
                'name': 'Эконом',
                'description': 'Простой и чистый номер с необходимыми удобствами',
                'price': 2000.00,
                'capacity': 2,
                'amenities': ['wifi', 'bathroom'],
                'available_count': 8
            },
            {
                'hotel': hotels[1],
                'name': 'Комфорт',
                'description': 'Номер с улучшенными удобствами и более просторной планировкой',
                'price': 3200.00,
                'capacity': 2,
                'amenities': ['wifi', 'tv', 'bathroom', 'conditioner'],
                'available_count': 5
            },
            {
                'hotel': hotels[1],
                'name': 'Семейный',
                'description': 'Просторный номер для семьи с детьми, две комнаты',
                'price': 4500.00,
                'capacity': 4,
                'amenities': ['wifi', 'tv', 'bathroom', 'conditioner', 'balcony'],
                'available_count': 3
            },
            # Морской Бриз
            {
                'hotel': hotels[2],
                'name': 'Стандарт с видом на море',
                'description': 'Номер с балконом и видом на Черное море',
                'price': 4500.00,
                'capacity': 2,
                'amenities': ['wifi', 'tv', 'minibar', 'conditioner', 'bathroom', 'balcony'],
                'available_count': 12
            },
            {
                'hotel': hotels[2],
                'name': 'Семейный люкс',
                'description': 'Просторный номер для семьи с видом на море, две спальни',
                'price': 8000.00,
                'capacity': 5,
                'amenities': ['wifi', 'tv', 'minibar', 'conditioner', 'safe', 'bathroom', 'balcony'],
                'available_count': 4
            },
            # Бизнес Центр
            {
                'hotel': hotels[3],
                'name': 'Стандарт',
                'description': 'Комфортный номер для деловых поездок',
                'price': 3000.00,
                'capacity': 1,
                'amenities': ['wifi', 'tv', 'bathroom', 'conditioner'],
                'available_count': 15
            },
            {
                'hotel': hotels[3],
                'name': 'Бизнес-класс',
                'description': 'Улучшенный номер с рабочим местом и видом на город',
                'price': 4500.00,
                'capacity': 2,
                'amenities': ['wifi', 'tv', 'minibar', 'conditioner', 'safe', 'bathroom'],
                'available_count': 8
            },
        ]

        room_types = []
        for room_data in room_types_data:
            room_type, created = RoomType.objects.get_or_create(
                hotel=room_data['hotel'],
                name=room_data['name'],
                defaults=room_data
            )
            room_types.append(room_type)
            self.stdout.write(f'  ✓ Номер: {room_type.hotel.name} - {room_type.name}')

        # Создаем резервирования
        self.stdout.write('Создание резервирований...')
        today = date.today()
        reservations_data = [
            {
                'user': users[0],
                'room_type': room_types[1],  # Стандартный двухместный Гранд Отель
                'check_in_date': today - timedelta(days=5),
                'check_out_date': today - timedelta(days=2),
                'status': 'checked_out'
            },
            {
                'user': users[1],
                'room_type': room_types[4],  # Комфорт Уютный Дворик
                'check_in_date': today - timedelta(days=3),
                'check_out_date': today + timedelta(days=2),
                'status': 'checked_in'
            },
            {
                'user': users[0],
                'room_type': room_types[7],  # Стандарт с видом на море
                'check_in_date': today + timedelta(days=5),
                'check_out_date': today + timedelta(days=10),
                'status': 'confirmed'
            },
            {
                'user': users[2],
                'room_type': room_types[2],  # Люкс Гранд Отель
                'check_in_date': today + timedelta(days=15),
                'check_out_date': today + timedelta(days=18),
                'status': 'pending'
            },
            {
                'user': users[1],
                'room_type': room_types[9],  # Бизнес-класс
                'check_in_date': today - timedelta(days=10),
                'check_out_date': today - timedelta(days=7),
                'status': 'checked_out'
            },
        ]

        reservations = []
        for res_data in reservations_data:
            reservation = Reservation.objects.create(**res_data)
            reservations.append(reservation)
            self.stdout.write(f'  ✓ Резервирование: {reservation.user.username} - {reservation.room_type.name}')

        # Создаем отзывы
        self.stdout.write('Создание отзывов...')
        reviews_data = [
            {
                'user': users[0],
                'room_type': room_types[1],  # Стандартный двухместный
                'reservation': reservations[0],
                'rating': 9,
                'comment': 'Отличный отель! Номер был чистым и просторным, вид на город потрясающий. Персонал очень дружелюбный и отзывчивый. Завтраки были разнообразными и вкусными. Обязательно вернемся!',
                'stay_period_start': reservations[0].check_in_date,
                'stay_period_end': reservations[0].check_out_date,
            },
            {
                'user': users[1],
                'room_type': room_types[4],  # Комфорт
                'rating': 8,
                'comment': 'Хороший отель за разумную цену. Номер чистый, удобная кровать. Расположение отличное - в центре города. Единственный минус - немного шумно ночью из-за центрального расположения.',
                'stay_period_start': today - timedelta(days=3),
                'stay_period_end': today + timedelta(days=2),
            },
            {
                'user': users[0],
                'room_type': room_types[2],  # Люкс
                'rating': 10,
                'comment': 'Превосходно! Люкс номер превзошел все ожидания. Огромная комната с панорамным видом, роскошная ванная комната, все удобства на высшем уровне. Персонал на высоте. Стоит своих денег!',
                'stay_period_start': today - timedelta(days=20),
                'stay_period_end': today - timedelta(days=17),
            },
            {
                'user': users[2],
                'room_type': room_types[7],  # Стандарт с видом на море
                'rating': 7,
                'comment': 'Неплохой отель у моря. Вид с балкона красивый, номер чистый. Но мебель немного устаревшая, и Wi-Fi работал нестабильно. В целом нормально для отдыха.',
                'stay_period_start': today - timedelta(days=30),
                'stay_period_end': today - timedelta(days=25),
            },
            {
                'user': users[1],
                'room_type': room_types[9],  # Бизнес-класс
                'reservation': reservations[4],
                'rating': 9,
                'comment': 'Отличный отель для деловых поездок. Удобное расположение, хороший Wi-Fi, тихие номера. Рабочее место в номере очень удобное. Рекомендую бизнесменам.',
                'stay_period_start': reservations[4].check_in_date,
                'stay_period_end': reservations[4].check_out_date,
            },
            {
                'user': users[0],
                'room_type': room_types[0],  # Стандартный одноместный
                'rating': 8,
                'comment': 'Хороший номер для одного человека. Все необходимое есть, чисто, тихо. Цена соответствует качеству. Подходит для коротких командировок.',
                'stay_period_start': today - timedelta(days=15),
                'stay_period_end': today - timedelta(days=13),
            },
        ]

        for review_data in reviews_data:
            review = Review.objects.create(**review_data)
            self.stdout.write(f'  ✓ Отзыв: {review.user.username} - рейтинг {review.rating}/10')

        self.stdout.write(self.style.SUCCESS('\n✓ Тестовые данные успешно загружены!'))
        self.stdout.write(f'\nСоздано:')
        self.stdout.write(f'  - Отелей: {len(hotels)}')
        self.stdout.write(f'  - Типов номеров: {len(room_types)}')
        self.stdout.write(f'  - Пользователей: {len(users)}')
        self.stdout.write(f'  - Резервирований: {len(reservations)}')
        self.stdout.write(f'  - Отзывов: {len(reviews_data)}')
        self.stdout.write(f'\nТестовые пользователи (пароль: test12345):')
        for user in users:
            self.stdout.write(f'  - {user.username} ({user.get_full_name()})')
