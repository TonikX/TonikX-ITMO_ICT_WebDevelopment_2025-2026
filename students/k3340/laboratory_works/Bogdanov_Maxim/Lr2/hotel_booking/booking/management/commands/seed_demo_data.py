from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from booking.models import Hotel, Amenity, RoomType, Room, Booking, Review
from datetime import date, timedelta
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Заполняет БД демонстрационными данными'

    def handle(self, *args, **options):
        self.stdout.write('Создание демо-данных...')

        # Очистка старых данных (опционально)
        if input('Очистить существующие данные? (y/n): ').lower() == 'y':
            Review.objects.all().delete()
            Booking.objects.all().delete()
            Room.objects.all().delete()
            RoomType.objects.all().delete()
            Hotel.objects.all().delete()
            Amenity.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS('Старые данные удалены'))

        # Пользователи
        users = []
        user_data = [
            ('ivan_petrov', 'ivan@example.com', 'Иван', 'Петров'),
            ('maria_sidorova', 'maria@example.com', 'Мария', 'Сидорова'),
            ('alex_ivanov', 'alex@example.com', 'Александр', 'Иванов'),
            ('elena_volkova', 'elena@example.com', 'Елена', 'Волкова'),
            ('dmitry_smirnov', 'dmitry@example.com', 'Дмитрий', 'Смирнов'),
            ('anna_kozlova', 'anna@example.com', 'Анна', 'Козлова'),
            ('sergey_morozov', 'sergey@example.com', 'Сергей', 'Морозов'),
            ('olga_novikova', 'olga@example.com', 'Ольга', 'Новикова'),
        ]

        for username, email, first_name, last_name in user_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name
                }
            )
            if created:
                user.set_password('demo1234')
                user.save()
                self.stdout.write(f'Создан пользователь: {username}')
            users.append(user)

        # Владельцы отелей
        owners = []
        owner_data = [
            ('hotel_owner1', 'owner1@example.com', 'Владимир', 'Владельцев'),
            ('hotel_owner2', 'owner2@example.com', 'Ирина', 'Гостиничная'),
            ('hotel_owner3', 'owner3@example.com', 'Михаил', 'Отельеров'),
        ]

        for username, email, first_name, last_name in owner_data:
            owner, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name
                }
            )
            if created:
                owner.set_password('owner1234')
                owner.save()
                self.stdout.write(f'Создан владелец: {username}')
            owners.append(owner)

        # Удобства
        amenities_data = [
            'Wi-Fi', 'Кондиционер', 'Телевизор', 'Холодильник', 'Сейф',
            'Балкон', 'Мини-бар', 'Джакузи', 'Фен', 'Утюг',
            'Халаты', 'Тапочки', 'Кофеварка', 'Микроволновка', 'Посудомоечная машина'
        ]
        amenities = {}
        for name in amenities_data:
            amenity, created = Amenity.objects.get_or_create(name=name)
            amenities[name] = amenity
            if created:
                self.stdout.write(f'Создано удобство: {name}')

        # Отели
        hotels_data = [
            ('Гранд Отель Москва', 'г. Москва, ул. Тверская, д. 1',
             'Роскошный отель в самом центре Москвы с видом на Кремль. Идеальное место для деловых поездок и туризма.'),
            ('Морской Бриз', 'г. Сочи, ул. Морская, д. 10',
             'Уютный отель на берегу Чёрного моря. Идеально подходит для семейного отдыха.'),
            ('Северная Звезда', 'г. Санкт-Петербург, Невский проспект, д. 50',
             'Элегантный отель в историческом центре Северной столицы.'),
            ('Золотое Кольцо', 'г. Владимир, ул. Большая Московская, д. 15',
             'Комфортабельный отель для путешественников по Золотому кольцу России.'),
            ('Байкал Резорт', 'Иркутская область, пос. Листвянка, ул. Озерная, д. 5',
             'Отель на берегу величественного озера Байкал с потрясающими видами.'),
            ('Казанский Дворец', 'г. Казань, ул. Баумана, д. 32',
             'Современный отель в центре Казани, рядом с Кремлём и пешеходной улицей.'),
            ('Уральские Горы', 'г. Екатеринбург, ул. Ленина, д. 24',
             'Отель для деловых и туристических поездок в столицу Урала.'),
            ('Волжский Простор', 'г. Нижний Новгород, Верхне-Волжская набережная, д. 2',
             'Отель с панорамным видом на Волгу и историческую часть города.'),
            ('Сибирский Экспресс', 'г. Новосибирск, Красный проспект, д. 18',
             'Удобный отель в центре Новосибирска для бизнеса и отдыха.'),
            ('Дальневосточный', 'г. Владивосток, ул. Светланская, д. 45',
             'Современный отель у бухты Золотой Рог с видом на море.'),
            ('Ростовский Купец', 'г. Ростов-на-Дону, Большая Садовая, д. 60',
             'Стильный отель в самом центре южной столицы России.'),
            ('Балтийский Берег', 'г. Калининград, пл. Победы, д. 10',
             'Отель в европейском стиле в самом западном городе России.'),
        ]

        hotels = []
        for i, (name, address, description) in enumerate(hotels_data):
            owner = owners[i % len(owners)]
            hotel, created = Hotel.objects.get_or_create(
                name=name,
                defaults={
                    'owner': owner,
                    'address': address,
                    'description': description
                }
            )
            if created:
                self.stdout.write(f'Создан отель: {name}')
            hotels.append(hotel)

        # Типы номеров и номера
        room_type_templates = [
            ('Эконом', 2, Decimal('1500'), ['Wi-Fi', 'Телевизор']),
            ('Стандарт', 2, Decimal('3000'), ['Wi-Fi', 'Телевизор', 'Кондиционер', 'Холодильник']),
            ('Стандарт Плюс', 3, Decimal('4000'), ['Wi-Fi', 'Телевизор', 'Кондиционер', 'Холодильник', 'Фен']),
            ('Комфорт', 3, Decimal('5500'),
             ['Wi-Fi', 'Телевизор', 'Кондиционер', 'Холодильник', 'Сейф', 'Балкон', 'Фен']),
            ('Бизнес', 2, Decimal('6500'),
             ['Wi-Fi', 'Телевизор', 'Кондиционер', 'Холодильник', 'Сейф', 'Мини-бар', 'Кофеварка']),
            ('Люкс', 4, Decimal('9000'),
             ['Wi-Fi', 'Телевизор', 'Кондиционер', 'Холодильник', 'Сейф', 'Балкон', 'Мини-бар', 'Джакузи', 'Халаты']),
            ('Премиум Люкс', 4, Decimal('12000'),
             ['Wi-Fi', 'Телевизор', 'Кондиционер', 'Холодильник', 'Сейф', 'Балкон', 'Мини-бар', 'Джакузи', 'Халаты',
              'Тапочки', 'Кофеварка']),
            ('Апартаменты', 6, Decimal('15000'),
             ['Wi-Fi', 'Телевизор', 'Кондиционер', 'Холодильник', 'Сейф', 'Балкон', 'Мини-бар', 'Микроволновка',
              'Посудомоечная машина', 'Кофеварка']),
        ]

        descriptions = [
            'Уютный номер с удобной кроватью и современным дизайном.',
            'Просторный номер с панорамными окнами.',
            'Элегантный номер с видом на город.',
            'Комфортабельный номер для семейного отдыха.',
            'Стильный номер для деловых путешественников.',
            'Роскошный номер с эксклюзивной мебелью.',
        ]

        all_rooms = []
        for hotel in hotels:
            # Случайно выбираем 4-6 типов номеров для каждого отеля
            num_types = random.randint(4, 6)
            selected_types = random.sample(room_type_templates, num_types)

            for type_name, capacity, base_price, amenity_names in selected_types:
                # Небольшая вариация цены для разных отелей
                price_variation = Decimal(random.uniform(0.8, 1.2))
                price = (base_price * price_variation).quantize(Decimal('0.01'))

                room_type, created = RoomType.objects.get_or_create(
                    hotel=hotel,
                    name=type_name,
                    defaults={
                        'capacity': capacity,
                        'price_per_night': price,
                        'description': random.choice(descriptions)
                    }
                )

                if created:
                    # Добавляем удобства
                    room_type.amenities.set([amenities[name] for name in amenity_names if name in amenities])
                    self.stdout.write(f'Создан тип номера: {hotel.name} - {type_name}')

                # Создаём 5-10 номеров каждого типа
                num_rooms = random.randint(5, 10)
                for i in range(num_rooms):
                    # Генерируем номер комнаты (этаж + номер)
                    floor = random.randint(1, 5)
                    room_num = random.randint(1, 20)
                    room_number = f"{floor}{room_num:02d}"

                    room, created = Room.objects.get_or_create(
                        room_type=room_type,
                        room_number=room_number
                    )

                    if created:
                        all_rooms.append(room)

        self.stdout.write(f'Создано {len(all_rooms)} номеров')

        # Бронирования
        today = date.today()
        bookings = []

        # Прошлые бронирования (выселены)
        for _ in range(50):
            user = random.choice(users)
            room = random.choice(all_rooms)
            days_ago = random.randint(30, 180)
            duration = random.randint(2, 7)

            check_in = today - timedelta(days=days_ago)
            check_out = check_in + timedelta(days=duration)

            booking = Booking(
                user=user,
                room=room,
                check_in=check_in,
                check_out=check_out,
                status='checked_out',
                total_price=room.room_type.price_per_night * duration
            )
            booking.save(skip_validation=True)
            bookings.append(booking)

        # Текущие бронирования (заселены)
        for _ in range(30):
            user = random.choice(users)
            room = random.choice(all_rooms)
            days_ago = random.randint(1, 5)
            duration = random.randint(3, 10)

            check_in = today - timedelta(days=days_ago)
            check_out = check_in + timedelta(days=duration)

            if check_out > today:  # Ещё не выселились
                booking = Booking(
                    user=user,
                    room=room,
                    check_in=check_in,
                    check_out=check_out,
                    status='checked_in',
                    total_price=room.room_type.price_per_night * duration
                )
                booking.save(skip_validation=True)
                bookings.append(booking)

        # Будущие бронирования (подтверждены)
        for _ in range(80):
            user = random.choice(users)
            room = random.choice(all_rooms)
            days_ahead = random.randint(1, 60)
            duration = random.randint(2, 14)

            check_in = today + timedelta(days=days_ahead)
            check_out = check_in + timedelta(days=duration)

            booking, created = Booking.objects.get_or_create(
                user=user,
                room=room,
                check_in=check_in,
                check_out=check_out,
                defaults={
                    'status': random.choice(['pending', 'confirmed']),
                    'total_price': room.room_type.price_per_night * duration
                }
            )
            if created:
                bookings.append(booking)

        self.stdout.write(f'Создано {len(bookings)} бронирований')

        # Отзывы
        review_comments = [
            'Отличный отель! Всё понравилось, персонал вежливый, номер чистый.',
            'Прекрасное расположение, рядом много достопримечательностей.',
            'Хороший отель для своей цены. Рекомендую!',
            'Комфортный номер, удобная кровать, хороший завтрак.',
            'Замечательный вид из окна! Обязательно вернёмся.',
            'Всё на высшем уровне: сервис, чистота, комфорт.',
            'Отель соответствует описанию. Спасибо за гостеприимство!',
            'Тихое и спокойное место, идеально для отдыха.',
            'Современный ремонт, хорошая звукоизоляция.',
            'Отличное соотношение цены и качества.',
            'Немного устаревший интерьер, но в целом всё хорошо.',
            'Персонал очень приветливый и всегда готов помочь.',
            'Чистота на высоте, уборка каждый день.',
            'Удобное расположение возле транспорта.',
            'Вкусные завтраки, большой выбор блюд.',
            'Тихий район, удобно для семейного отдыха.',
            'Номер просторный, есть всё необходимое.',
            'Рядом много кафе и ресторанов.',
            'За эту цену лучше не найти!',
            'Всё понравилось, единственный минус - слабый Wi-Fi.',
            'Отличный отель для деловых поездок.',
            'Красивый вид, комфортная атмосфера.',
            'Немного шумно, но терпимо.',
            'Хорошее место для отдыха всей семьёй.',
            'Приятно удивлены качеством обслуживания.',
        ]

        reviews = []
        # Создаём отзывы только для завершённых броней
        completed_bookings = [b for b in bookings if b.status == 'checked_out']

        for _ in range(min(100, len(completed_bookings))):
            booking = random.choice(completed_bookings)

            # Проверяем, нет ли уже отзыва на это бронирование
            if Review.objects.filter(booking=booking).exists():
                continue

            rating = random.randint(6, 10)  # Большинство отзывов положительные
            if random.random() < 0.2:  # 20% средних отзывов
                rating = random.randint(4, 6)

            review = Review(
                user=booking.user,
                room=booking.room,
                booking=booking,
                stay_start=booking.check_in,
                stay_end=booking.check_out,
                rating=rating,
                comment=random.choice(review_comments)
            )
            review.save()
            reviews.append(review)

            completed_bookings.remove(booking)  # Убираем, чтобы не повторяться

        self.stdout.write(f'Создано {len(reviews)} отзывов')

        # Итоговая статистика
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 50))
        self.stdout.write(self.style.SUCCESS('Демо-данные успешно созданы!'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(f'Пользователей: {User.objects.count()}')
        self.stdout.write(f'Отелей: {Hotel.objects.count()}')
        self.stdout.write(f'Типов номеров: {RoomType.objects.count()}')
        self.stdout.write(f'Номеров: {Room.objects.count()}')
        self.stdout.write(f'Бронирований: {Booking.objects.count()}')
        self.stdout.write(f'Отзывов: {Review.objects.count()}')
        self.stdout.write(f'Удобств: {Amenity.objects.count()}')
        self.stdout.write('\n' + 'Тестовые учётные данные:')
        self.stdout.write('  Пользователи: ivan_petrov, maria_sidorova, и др. / demo1234')
        self.stdout.write('  Владельцы: hotel_owner1, hotel_owner2, hotel_owner3 / owner1234')