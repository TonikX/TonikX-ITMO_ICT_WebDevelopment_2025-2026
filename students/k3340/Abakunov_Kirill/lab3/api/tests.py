"""
Тесты для API
"""
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Room, Guest, Staff, CleaningSchedule
from datetime import date, timedelta


class RoomAPITestCase(TestCase):
    """Тесты для API номеров"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('testuser', 'test@test.com', 'testpass')
        self.client.force_authenticate(user=self.user)
        
        self.room = Room.objects.create(
            number='101',
            room_type='single',
            floor=1,
            phone='+7 (495) 123-45-67',
            price_per_day=2500
        )
    
    def test_list_rooms(self):
        """Тест получения списка номеров"""
        response = self.client.get('/api/rooms/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    def test_get_available_rooms(self):
        """Тест получения свободных номеров"""
        response = self.client.get('/api/rooms/available/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    def test_create_room(self):
        """Тест создания номера"""
        data = {
            'number': '102',
            'room_type': 'double',
            'floor': 1,
            'phone': '+7 (495) 123-45-68',
            'price_per_day': '3500.00'
        }
        response = self.client.post('/api/rooms/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Room.objects.count(), 2)


class GuestAPITestCase(TestCase):
    """Тесты для API клиентов"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('testuser', 'test@test.com', 'testpass')
        self.client.force_authenticate(user=self.user)
        
        self.room = Room.objects.create(
            number='101',
            room_type='single',
            floor=1,
            phone='+7 (495) 123-45-67',
            price_per_day=2500
        )
        
        self.guest = Guest.objects.create(
            passport_number='1234 567890',
            last_name='Иванов',
            first_name='Иван',
            middle_name='Иванович',
            city='Москва',
            room=self.room,
            check_in_date=date.today()
        )
    
    def test_list_guests(self):
        """Тест получения списка клиентов"""
        response = self.client.get('/api/guests/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    def test_check_in_guest(self):
        """Тест поселения клиента"""
        room2 = Room.objects.create(
            number='102',
            room_type='double',
            floor=1,
            phone='+7 (495) 123-45-68',
            price_per_day=3500
        )
        
        data = {
            'passport_number': '9999 888777',
            'last_name': 'Петров',
            'first_name': 'Петр',
            'middle_name': 'Петрович',
            'city': 'Санкт-Петербург',
            'room': room2.id,
            'check_in_date': date.today().isoformat()
        }
        response = self.client.post('/api/guests/check_in/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Guest.objects.count(), 2)
    
    def test_check_out_guest(self):
        """Тест выселения клиента"""
        data = {
            'check_out_date': (date.today() + timedelta(days=5)).isoformat()
        }
        response = self.client.patch(f'/api/guests/{self.guest.id}/check_out/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.guest.refresh_from_db()
        self.assertIsNotNone(self.guest.check_out_date)
    
    def test_from_city(self):
        """Тест поиска клиентов из города"""
        response = self.client.get('/api/guests/from_city/?city=Москва')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)


class StaffAPITestCase(TestCase):
    """Тесты для API служащих"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('testuser', 'test@test.com', 'testpass')
        self.client.force_authenticate(user=self.user)
        
        self.staff = Staff.objects.create(
            last_name='Петров',
            first_name='Петр',
            middle_name='Петрович',
            hire_date=date.today(),
            is_active=True
        )
    
    def test_list_staff(self):
        """Тест получения списка служащих"""
        response = self.client.get('/api/staff/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    def test_hire_staff(self):
        """Тест приема служащего на работу"""
        data = {
            'last_name': 'Сидоров',
            'first_name': 'Сидор',
            'middle_name': 'Сидорович',
            'hire_date': date.today().isoformat()
        }
        response = self.client.post('/api/staff/hire/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Staff.objects.count(), 2)
    
    def test_fire_staff(self):
        """Тест увольнения служащего"""
        data = {
            'fire_date': date.today().isoformat()
        }
        response = self.client.patch(f'/api/staff/{self.staff.id}/fire/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.staff.refresh_from_db()
        self.assertFalse(self.staff.is_active)


class CleaningScheduleAPITestCase(TestCase):
    """Тесты для API расписания уборки"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('testuser', 'test@test.com', 'testpass')
        self.client.force_authenticate(user=self.user)
        
        self.staff = Staff.objects.create(
            last_name='Петров',
            first_name='Петр',
            middle_name='Петрович',
            hire_date=date.today(),
            is_active=True
        )
        
        self.schedule = CleaningSchedule.objects.create(
            staff=self.staff,
            floor=1,
            weekday=1
        )
    
    def test_list_schedules(self):
        """Тест получения списка расписаний"""
        response = self.client.get('/api/schedules/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    def test_by_floor(self):
        """Тест получения расписания по этажу"""
        response = self.client.get('/api/schedules/by_floor/?floor=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['schedules']), 1)
    
    def test_by_weekday(self):
        """Тест получения расписания по дню недели"""
        response = self.client.get('/api/schedules/by_weekday/?weekday=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['schedules']), 1)
