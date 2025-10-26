from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date, timedelta
from .models import Hotel, RoomType, Room, Booking, Review, Amenity
from .services import check_room_availability, get_available_rooms
from django.core.exceptions import ValidationError


class BookingAvailabilityTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='test123')
        self.owner = User.objects.create_user(username='owner', password='owner123')

        self.hotel = Hotel.objects.create(
            name='Test Hotel',
            owner=self.owner,
            address='Test Address'
        )

        self.room_type = RoomType.objects.create(
            hotel=self.hotel,
            name='Standard',
            capacity=2,
            price_per_night=100
        )

        self.room = Room.objects.create(
            room_type=self.room_type,
            room_number='101'
        )

    def test_room_available_no_bookings(self):
        """Номер доступен, если нет бронирований"""
        check_in = date.today() + timedelta(days=1)
        check_out = date.today() + timedelta(days=3)

        self.assertTrue(check_room_availability(self.room, check_in, check_out))

    def test_room_unavailable_overlapping_confirmed(self):
        """Номер недоступен при пересечении с подтверждённой бронью"""
        Booking.objects.create(
            user=self.user,
            room=self.room,
            check_in=date.today() + timedelta(days=2),
            check_out=date.today() + timedelta(days=5),
            status='confirmed',
            total_price=300
        )

        check_in = date.today() + timedelta(days=1)
        check_out = date.today() + timedelta(days=3)

        self.assertFalse(check_room_availability(self.room, check_in, check_out))

    def test_room_available_cancelled_booking(self):
        """Номер доступен, если существующая бронь отменена"""
        Booking.objects.create(
            user=self.user,
            room=self.room,
            check_in=date.today() + timedelta(days=2),
            check_out=date.today() + timedelta(days=5),
            status='cancelled',
            total_price=300
        )

        check_in = date.today() + timedelta(days=1)
        check_out = date.today() + timedelta(days=3)

        self.assertTrue(check_room_availability(self.room, check_in, check_out))

    def test_room_available_no_overlap(self):
        """Номер доступен, если даты не пересекаются"""
        Booking.objects.create(
            user=self.user,
            room=self.room,
            check_in=date.today() + timedelta(days=1),
            check_out=date.today() + timedelta(days=3),
            status='confirmed',
            total_price=200
        )

        # Бронируем после существующей брони
        check_in = date.today() + timedelta(days=3)
        check_out = date.today() + timedelta(days=5)

        self.assertTrue(check_room_availability(self.room, check_in, check_out))


class BookingValidationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='test123')
        self.owner = User.objects.create_user(username='owner', password='owner123')

        self.hotel = Hotel.objects.create(
            name='Test Hotel',
            owner=self.owner,
            address='Test Address'
        )

        self.room_type = RoomType.objects.create(
            hotel=self.hotel,
            name='Standard',
            capacity=2,
            price_per_night=100
        )

        self.room = Room.objects.create(
            room_type=self.room_type,
            room_number='101'
        )

    def test_check_out_before_check_in_invalid(self):
        """Дата выезда раньше заезда - невалидно"""
        booking = Booking(
            user=self.user,
            room=self.room,
            check_in=date.today() + timedelta(days=5),
            check_out=date.today() + timedelta(days=3),
            status='pending',
            total_price=200
        )

        with self.assertRaises(ValidationError):
            booking.full_clean()

    def test_check_in_in_past_invalid(self):
        """Дата заезда в прошлом - невалидно при создании"""
        booking = Booking(
            user=self.user,
            room=self.room,
            check_in=date.today() - timedelta(days=1),
            check_out=date.today() + timedelta(days=2),
            status='pending',
            total_price=300
        )

        with self.assertRaises(ValidationError):
            booking.full_clean()


class ReviewValidationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='test123')
        self.owner = User.objects.create_user(username='owner', password='owner123')

        self.hotel = Hotel.objects.create(
            name='Test Hotel',
            owner=self.owner,
            address='Test Address'
        )

        self.room_type = RoomType.objects.create(
            hotel=self.hotel,
            name='Standard',
            capacity=2,
            price_per_night=100
        )

        self.room = Room.objects.create(
            room_type=self.room_type,
            room_number='101'
        )

    def test_review_after_check_in_valid(self):
        """Отзыв валиден после даты заезда"""
        # Создаём бронирование с пропуском валидации
        booking = Booking(
            user=self.user,
            room=self.room,
            check_in=date.today() - timedelta(days=5),
            check_out=date.today() + timedelta(days=2),
            status='checked_in',
            total_price=700
        )
        booking.save(skip_validation=True)

        review = Review(
            user=self.user,
            room=self.room,
            booking=booking,
            stay_start=booking.check_in,
            stay_end=booking.check_out,
            rating=8,
            comment='Great stay!'
        )

        # Не должно выбросить исключение
        review.full_clean()

    def test_review_before_check_in_invalid(self):
        """Отзыв нельзя оставить до даты заезда"""
        booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            check_in=date.today() + timedelta(days=5),
            check_out=date.today() + timedelta(days=7),
            status='confirmed',
            total_price=200
        )

        review = Review(
            user=self.user,
            room=self.room,
            booking=booking,
            stay_start=booking.check_in,
            stay_end=booking.check_out,
            rating=8,
            comment='Test'
        )

        with self.assertRaises(ValidationError):
            review.full_clean()

    def test_review_rating_validation(self):
        """Рейтинг должен быть от 1 до 10"""
        # Создаём бронирование с пропуском валидации
        booking = Booking(
            user=self.user,
            room=self.room,
            check_in=date.today() - timedelta(days=5),
            check_out=date.today() - timedelta(days=2),
            status='checked_out',
            total_price=300
        )
        booking.save(skip_validation=True)

        # Рейтинг < 1
        review = Review(
            user=self.user,
            room=self.room,
            booking=booking,
            stay_start=booking.check_in,
            stay_end=booking.check_out,
            rating=0,
            comment='Test'
        )

        with self.assertRaises(ValidationError):
            review.full_clean()

        # Рейтинг > 10
        review.rating = 11
        with self.assertRaises(ValidationError):
            review.full_clean()

        # Валидный рейтинг
        review.rating = 8
        review.full_clean()  # Не должно выбросить исключение


class UserPermissionsTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass1')
        self.user2 = User.objects.create_user(username='user2', password='pass2')
        self.owner = User.objects.create_user(username='owner', password='owner123')

        self.hotel = Hotel.objects.create(
            name='Test Hotel',
            owner=self.owner,
            address='Test Address'
        )

        self.room_type = RoomType.objects.create(
            hotel=self.hotel,
            name='Standard',
            capacity=2,
            price_per_night=100
        )

        self.room = Room.objects.create(
            room_type=self.room_type,
            room_number='101'
        )

    def test_user_can_only_see_own_bookings(self):
        """Пользователь видит только свои бронирования"""
        booking1 = Booking.objects.create(
            user=self.user1,
            room=self.room,
            check_in=date.today() + timedelta(days=1),
            check_out=date.today() + timedelta(days=3),
            status='confirmed',
            total_price=200
        )

        booking2 = Booking.objects.create(
            user=self.user2,
            room=self.room,
            check_in=date.today() + timedelta(days=5),
            check_out=date.today() + timedelta(days=7),
            status='confirmed',
            total_price=200
        )

        user1_bookings = Booking.objects.filter(user=self.user1)
        self.assertEqual(user1_bookings.count(), 1)
        self.assertEqual(user1_bookings.first().id, booking1.id)


class GetAvailableRoomsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='test123')
        self.owner = User.objects.create_user(username='owner', password='owner123')

        self.hotel = Hotel.objects.create(
            name='Test Hotel',
            owner=self.owner,
            address='Test Address'
        )

        self.room_type = RoomType.objects.create(
            hotel=self.hotel,
            name='Standard',
            capacity=2,
            price_per_night=100
        )

        self.room1 = Room.objects.create(
            room_type=self.room_type,
            room_number='101'
        )

        self.room2 = Room.objects.create(
            room_type=self.room_type,
            room_number='102'
        )

    def test_get_available_rooms_filters_booked(self):
        """get_available_rooms исключает занятые номера"""
        Booking.objects.create(
            user=self.user,
            room=self.room1,
            check_in=date.today() + timedelta(days=1),
            check_out=date.today() + timedelta(days=3),
            status='confirmed',
            total_price=200
        )

        check_in = date.today() + timedelta(days=1)
        check_out = date.today() + timedelta(days=3)

        available = get_available_rooms(check_in, check_out)

        self.assertEqual(available.count(), 1)
        self.assertEqual(available.first().id, self.room2.id)


class ReviewFromBookingTestCase(TestCase):
    """Тесты для новой логики создания отзывов из бронирований"""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='test123')
        self.owner = User.objects.create_user(username='owner', password='owner123')

        self.hotel = Hotel.objects.create(
            name='Test Hotel',
            owner=self.owner,
            address='Test Address'
        )

        self.room_type = RoomType.objects.create(
            hotel=self.hotel,
            name='Standard',
            capacity=2,
            price_per_night=100
        )

        self.room = Room.objects.create(
            room_type=self.room_type,
            room_number='101'
        )

    def test_can_review_after_check_in(self):
        """Можно оставить отзыв после заезда"""
        # Создаём бронирование с заездом в прошлом, пропуская валидацию
        booking = Booking(
            user=self.user,
            room=self.room,
            check_in=date.today() - timedelta(days=2),
            check_out=date.today() + timedelta(days=3),
            status='checked_in',
            total_price=500
        )
        booking.save(skip_validation=True)

        # Создаём отзыв
        review = Review(
            user=self.user,
            room=self.room,
            booking=booking,
            stay_start=booking.check_in,
            stay_end=booking.check_out,
            rating=9,
            comment='Excellent!'
        )

        # Не должно выбросить исключение
        review.full_clean()
        review.save()

        self.assertEqual(Review.objects.filter(booking=booking).count(), 1)

    def test_cannot_review_before_check_in(self):
        """Нельзя оставить отзыв до заезда"""
        booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            check_in=date.today() + timedelta(days=2),
            check_out=date.today() + timedelta(days=5),
            status='confirmed',
            total_price=300
        )

        review = Review(
            user=self.user,
            room=self.room,
            booking=booking,
            stay_start=booking.check_in,
            stay_end=booking.check_out,
            rating=9,
            comment='Test'
        )

        with self.assertRaises(ValidationError):
            review.full_clean()