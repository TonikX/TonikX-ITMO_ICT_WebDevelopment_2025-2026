"""
Тесты моделей приложения racing.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from datetime import date, timedelta
from racing.models import Team, DriverProfile, Race, Heat, Registration, Comment


class TeamModelTest(TestCase):
    """Тесты модели Team."""
    
    def test_team_creation(self):
        """Тест создания команды."""
        team = Team.objects.create(name='Тестовая команда', description='Описание')
        self.assertEqual(str(team), 'Тестовая команда')
        self.assertTrue(team.pk)
    
    def test_team_unique_name(self):
        """Тест уникальности названия команды."""
        Team.objects.create(name='Команда')
        with self.assertRaises(IntegrityError):
            Team.objects.create(name='Команда')


class DriverProfileModelTest(TestCase):
    """Тесты модели DriverProfile."""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
    
    def test_driver_profile_auto_creation(self):
        """Тест автосоздания профиля при создании пользователя."""
        user = User.objects.create_user(username='newuser', password='12345')
        self.assertTrue(hasattr(user, 'driver_profile'))
        self.assertIsNotNone(user.driver_profile)
    
    def test_driver_profile_str(self):
        """Тест строкового представления профиля."""
        profile = self.user.driver_profile
        profile.full_name = 'Иван Иванов'
        profile.save()
        self.assertIn('Иван Иванов', str(profile))
        self.assertIn('testuser', str(profile))


class RaceModelTest(TestCase):
    """Тесты модели Race."""
    
    def test_race_creation(self):
        """Тест создания гонки."""
        race = Race.objects.create(
            title='Тестовая гонка',
            location='Москва',
            date=date.today(),
            is_published=True
        )
        self.assertEqual(str(race), f'Тестовая гонка ({date.today()})')


class RegistrationModelTest(TestCase):
    """Тесты модели Registration."""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.race = Race.objects.create(
            title='Гонка',
            location='Москва',
            date=date.today()
        )
    
    def test_registration_unique_constraint(self):
        """Тест уникальности регистрации driver+race."""
        Registration.objects.create(
            driver=self.user.driver_profile,
            race=self.race
        )
        with self.assertRaises(IntegrityError):
            Registration.objects.create(
                driver=self.user.driver_profile,
                race=self.race
            )


class CommentModelTest(TestCase):
    """Тесты модели Comment."""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.race = Race.objects.create(
            title='Гонка',
            location='Москва',
            date=date.today()
        )
    
    def test_comment_creation(self):
        """Тест создания комментария."""
        comment = Comment.objects.create(
            race=self.race,
            author=self.user,
            heat_date=date.today(),
            kind='race',
            rating=8,
            text='Отличная гонка!'
        )
        self.assertTrue(comment.pk)
        self.assertEqual(comment.rating, 8)
    
    def test_comment_rating_validation(self):
        """Тест валидации рейтинга."""
        comment = Comment(
            race=self.race,
            author=self.user,
            heat_date=date.today(),
            kind='race',
            rating=11,  # Неверное значение
            text='Текст'
        )
        with self.assertRaises(ValidationError):
            comment.full_clean()

