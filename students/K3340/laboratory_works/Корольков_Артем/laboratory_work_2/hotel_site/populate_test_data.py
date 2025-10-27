import os
import django
import random
from datetime import datetime, timedelta
from django.utils import timezone

# Настройка окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_site.settings')
django.setup()

from django.contrib.auth.models import User
from hotels.models import Hotel, RoomType, Reservation, Review


def create_test_users():
    """Создание тестовых пользователей"""
    users_data = [
        {'username': 'test_user', 'password': 'password123', 'email': 'user@example.com'},
        {'username': 'john_doe', 'password': 'password123', 'email': 'john@example.com'},
        {'username': 'alice_smith', 'password': 'password123', 'email': 'alice@example.com'},
        {'username': 'bob_johnson', 'password': 'password123', 'email': 'bob@example.com'},
    ]

    created_users = []
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={'email': user_data['email']}
        )
        if created:
            user.set_password(user_data['password'])
            user.save()
            print(f"Создан пользователь: {user.username}")
        else:
            print(f"Пользователь {user.username} уже существует")
        created_users.append(user)

    return created_users


def create_hotels():
    """Создание 20 отелей с разными типами номеров"""
    hotels_data = [
        {
            'name': 'Гранд Отель Европа',
            'owner': 'Иван Петров',
            'address': 'Москва, ул. Тверская, 1',
            'description': 'Роскошный пятизвездочный отель в центре Москвы с видом на Кремль',
            'amenities': 'WiFi, бассейн, спа, ресторан, фитнес-центр, консьерж-сервис'
        },
        {
            'name': 'Азимут Отель',
            'owner': 'Мария Сидорова',
            'address': 'Санкт-Петербург, Невский проспект, 25',
            'description': 'Современный отель в историческом центре Санкт-Петербурга',
            'amenities': 'WiFi, ресторан, парковка, бизнес-центр'
        },
        {
            'name': 'Нева Плаза',
            'owner': 'Алексей Козлов',
            'address': 'Санкт-Петербург, набережная реки Мойки, 15',
            'description': 'Элегантный отель с видом на реку Мойку',
            'amenities': 'WiFi, завтрак включен, терраса, трансфер'
        },
        {
            'name': 'Метрополь',
            'owner': 'Ольга Новикова',
            'address': 'Москва, Театральный проезд, 2',
            'description': 'Исторический отель с архитектурой модерн',
            'amenities': 'WiFi, ресторан, спа, исторические номера'
        },
        {
            'name': 'Балтийская Звезда',
            'owner': 'Дмитрий Волков',
            'address': 'Калининград, Ленинский проспект, 81',
            'description': 'Современный отель в центре Калининграда',
            'amenities': 'WiFi, парковка, конференц-зал, бар'
        },
        {
            'name': 'Уральские Зори',
            'owner': 'Сергей Павлов',
            'address': 'Екатеринбург, ул. Ленина, 52',
            'description': 'Комфортабельный отель для деловых поездок',
            'amenities': 'WiFi, бизнес-центр, прачечная, кафе'
        },
        {
            'name': 'Сибирь Холидей',
            'owner': 'Наталья Морозова',
            'address': 'Новосибирск, Красный проспект, 35',
            'description': 'Отель для отдыха и бизнеса в центре Новосибирска',
            'amenities': 'WiFi, фитнес, сауна, ресторан'
        },
        {
            'name': 'Волга Премиум',
            'owner': 'Андрей Семенов',
            'address': 'Нижний Новгород, ул. Большая Покровская, 15',
            'description': 'Отель в пешеходной зоне исторического центра',
            'amenities': 'WiFi, завтрак, экскурсии, сувенирный магазин'
        },
        {
            'name': 'Сочи Марин',
            'owner': 'Елена Ковалева',
            'address': 'Сочи, ул. Курортный проспект, 103',
            'description': 'Курортный отель с видом на море',
            'amenities': 'WiFi, бассейн, пляж, спа, анимация'
        },
        {
            'name': 'Казань Палас',
            'owner': 'Руслан Хакимов',
            'address': 'Казань, ул. Баумана, 35',
            'description': 'Отель в сердце исторического центра Казани',
            'amenities': 'WiFi, хаммам, ресторан татарской кухни'
        },
        {
            'name': 'Крымские Ворота',
            'owner': 'Анна Петренко',
            'address': 'Симферополь, ул. Киевская, 115',
            'description': 'Уютный отель для отдыха в Крыму',
            'amenities': 'WiFi, парковка, трансфер, экскурсии'
        },
        {
            'name': 'Байкал Лодж',
            'owner': 'Виктор Иванов',
            'address': 'Иркутск, ул. Лермонтова, 45',
            'description': 'Эко-отель для любителей природы Байкала',
            'amenities': 'WiFi, экскурсии, прокат оборудования, камин'
        },
        {
            'name': 'Арктик Скай',
            'owner': 'Олег Северов',
            'address': 'Мурманск, пр. Ленина, 82',
            'description': 'Отель с видом на северное сияние',
            'amenities': 'WiFi, сауна, ресторан северной кухни'
        },
        {
            'name': 'Домодедово Бизнес',
            'owner': 'Павел Алексеев',
            'address': 'Москва, г. Домодедово, ул. Аэропорт, 1',
            'description': 'Удобный отель рядом с аэропортом',
            'amenities': 'WiFi, трансфер, ранний заезд, бизнес-центр'
        },
        {
            'name': 'Золотое Кольцо',
            'owner': 'Татьяна Орлова',
            'address': 'Ярославль, ул. Свободы, 25',
            'description': 'Отель на маршруте Золотого Кольца России',
            'amenities': 'WiFi, экскурсии, сувениры, русская баня'
        },
        {
            'name': 'Алтай Ресорт',
            'owner': 'Геннадий Степанов',
            'address': 'Горно-Алтайск, ул. Чорос-Гуркина, 38',
            'description': 'Горный курорт в сердце Алтая',
            'amenities': 'WiFi, баня, походы, прокат велосипедов'
        },
        {
            'name': 'Сахалин Оушен',
            'owner': 'Марина Тихонова',
            'address': 'Южно-Сахалинск, ул. Ленина, 154',
            'description': 'Отель на острове Сахалин с морской тематикой',
            'amenities': 'WiFi, дайвинг, рыбалка, морские экскурсии'
        },
        {
            'name': 'Кубань Станица',
            'owner': 'Владимир Чернов',
            'address': 'Краснодар, ул. Красная, 115',
            'description': 'Отель в кубанском стиле с местным колоритом',
            'amenities': 'WiFi, казачья кухня, фольклорные программы'
        },
        {
            'name': 'Северная Столица',
            'owner': 'Екатерина Романова',
            'address': 'Санкт-Петербург, ул. Миллионная, 12',
            'description': 'Бутик-отель в дворцовом стиле',
            'amenities': 'WiFi, антикварная мебель, индивидуальный сервис'
        },
        {
            'name': 'Москва Сити Тауэр',
            'owner': 'Артем Корольков',
            'address': 'Москва, Пресненская наб., 8',
            'description': 'Современный отель в небоскребе Москва-Сити',
            'amenities': 'WiFi, панорамный вид, спа, премиум ресторан'
        }
    ]

    room_types = [
        {'name': 'Стандарт', 'cost_multiplier': 1.0, 'capacity': 2},
        {'name': 'Улучшенный', 'cost_multiplier': 1.5, 'capacity': 2},
        {'name': 'Люкс', 'cost_multiplier': 2.5, 'capacity': 3},
        {'name': 'Президентский люкс', 'cost_multiplier': 4.0, 'capacity': 4},
        {'name': 'Семейный', 'cost_multiplier': 1.8, 'capacity': 4},
    ]

    created_hotels = []

    for hotel_data in hotels_data:
        hotel, created = Hotel.objects.get_or_create(
            name=hotel_data['name'],
            defaults={
                'owner': hotel_data['owner'],
                'address': hotel_data['address'],
                'description': hotel_data['description'],
                'amenities': hotel_data['amenities']
            }
        )

        if created:
            print(f"Создан отель: {hotel.name}")

            # Создаем типы номеров для отеля
            base_cost = random.randint(2000, 5000)
            for room_type_data in room_types:
                cost = int(base_cost * room_type_data['cost_multiplier'])
                RoomType.objects.create(
                    hotel=hotel,
                    name=room_type_data['name'],
                    cost=cost,
                    capacity=room_type_data['capacity']
                )
            print(f"  → Созданы типы номеров для {hotel.name}")
        else:
            print(f"Отель {hotel.name} уже существует")

        created_hotels.append(hotel)

    return created_hotels


def create_reservations(users, hotels):
    """Создание тестовых бронирований"""
    reservations_data = []

    # Получаем все типы номеров
    room_types = RoomType.objects.all()

    if not room_types:
        print("Нет типов номеров для создания бронирований!")
        return []

    # Создаем бронирования для test_user
    test_user = users[0]  # test_user

    # Прошлые бронирования (завершенные)
    past_dates = [
        (timezone.now().date() - timedelta(days=45), timezone.now().date() - timedelta(days=40)),
        (timezone.now().date() - timedelta(days=30), timezone.now().date() - timedelta(days=25)),
        (timezone.now().date() - timedelta(days=15), timezone.now().date() - timedelta(days=10)),
    ]

    for check_in, check_out in past_dates:
        room_type = random.choice(room_types)
        reservation = Reservation.objects.create(
            user=test_user,
            room_type=room_type,
            check_in=check_in,
            check_out=check_out,
            status='checked_out'
        )
        reservations_data.append(reservation)
        print(f"Создано прошедшее бронирование для {test_user.username}: {room_type.hotel.name}")

    # Текущие бронирования
    current_dates = [
        (timezone.now().date() - timedelta(days=2), timezone.now().date() + timedelta(days=3)),
        (timezone.now().date() + timedelta(days=5), timezone.now().date() + timedelta(days=10)),
    ]

    for check_in, check_out in current_dates:
        room_type = random.choice(room_types)
        reservation = Reservation.objects.create(
            user=test_user,
            room_type=room_type,
            check_in=check_in,
            check_out=check_out,
            status='confirmed'
        )
        reservations_data.append(reservation)
        print(f"Создано текущее бронирование для {test_user.username}: {room_type.hotel.name}")

    # Создаем бронирования для других пользователей
    for user in users[1:]:  # остальные пользователи
        for _ in range(2):
            check_in = timezone.now().date() + timedelta(days=random.randint(1, 30))
            check_out = check_in + timedelta(days=random.randint(1, 7))
            room_type = random.choice(room_types)

            reservation = Reservation.objects.create(
                user=user,
                room_type=room_type,
                check_in=check_in,
                check_out=check_out,
                status=random.choice(['confirmed', 'checked_in'])
            )
            reservations_data.append(reservation)
            print(f"Создано бронирование для {user.username}: {room_type.hotel.name}")

    return reservations_data


def create_reviews(users, reservations):
    """Создание тестовых отзывов"""
    reviews_data = []

    # Создаем отзывы для завершенных бронирований
    completed_reservations = [r for r in reservations if r.status == 'checked_out']

    for reservation in completed_reservations[:8]:  # 8 отзывов
        stay_period = f"{reservation.check_in.strftime('%d.%m.%Y')} - {reservation.check_out.strftime('%d.%m.%Y')}"
        review = Review.objects.create(
            user=reservation.user,
            room_type=reservation.room_type,
            stay_period=stay_period,
            text=f"Отличный отель {reservation.room_type.hotel.name}! {random.choice(['Очень понравилось обслуживание.', 'Прекрасные номера.', 'Великолепный вид из окна.', 'Удобное расположение.'])}",
            rating=random.randint(7, 10)
        )
        reviews_data.append(review)
        print(f"Создан отзыв от {reservation.user.username} для {reservation.room_type.hotel.name}")

    return reviews_data


def main():
    """Основная функция заполнения данными"""
    print("=" * 50)
    print("НАЧАЛО ЗАПОЛНЕНИЯ ТЕСТОВЫМИ ДАННЫМИ")
    print("=" * 50)

    try:
        # Создаем пользователей
        print("\n1. СОЗДАНИЕ ПОЛЬЗОВАТЕЛЕЙ...")
        users = create_test_users()

        # Создаем отели
        print("\n2. СОЗДАНИЕ ОТЕЛЕЙ...")
        hotels = create_hotels()

        # Создаем бронирования
        print("\n3. СОЗДАНИЕ БРОНИРОВАНИЙ...")
        reservations = create_reservations(users, hotels)

        # Создаем отзывы
        print("\n4. СОЗДАНИЕ ОТЗЫВОВ...")
        reviews = create_reviews(users, reservations)

        print("\n" + "=" * 50)
        print("ЗАПОЛНЕНИЕ ДАННЫМИ ЗАВЕРШЕНО!")
        print("=" * 50)
        print(f"Создано/найдено:")
        print(f"  - Пользователей: {len(users)}")
        print(f"  - Отелей: {len(hotels)}")
        print(f"  - Типов номеров: {RoomType.objects.count()}")
        print(f"  - Бронирований: {len(reservations)}")
        print(f"  - Отзывов: {len(reviews)}")
        print("\nДанные для входа:")
        print("  Обычный пользователь: test_user / password123")
        print("  Другие пользователи: john_doe, alice_smith, bob_johnson / password123")
        print("=" * 50)

    except Exception as e:
        print(f"\nОШИБКА: {e}")
        print("Проверьте настройки Django и модели")


if __name__ == '__main__':
    main()