"""
Тесты форм приложения racing.
"""
from django.test import TestCase
from datetime import date
from racing.forms import CommentForm, DriverProfileForm


class CommentFormTest(TestCase):
    """Тесты формы комментария."""
    
    def test_valid_comment_form(self):
        """Тест валидной формы."""
        form = CommentForm(data={
            'heat_date': date.today(),
            'kind': 'race',
            'rating': 8,
            'text': 'Отличная гонка!'
        })
        self.assertTrue(form.is_valid())
    
    def test_invalid_rating_too_high(self):
        """Тест невалидного рейтинга (слишком высокий)."""
        form = CommentForm(data={
            'heat_date': date.today(),
            'kind': 'race',
            'rating': 11,
            'text': 'Текст'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)
    
    def test_invalid_rating_too_low(self):
        """Тест невалидного рейтинга (слишком низкий)."""
        form = CommentForm(data={
            'heat_date': date.today(),
            'kind': 'race',
            'rating': 0,
            'text': 'Текст'
        })
        self.assertFalse(form.is_valid())


class DriverProfileFormTest(TestCase):
    """Тесты формы профиля водителя."""
    
    def test_valid_profile_form(self):
        """Тест валидной формы профиля."""
        form = DriverProfileForm(data={
            'full_name': 'Иван Иванов',
            'car_description': 'BMW M3',
            'bio': 'Опытный гонщик',
            'experience_years': 5,
            'driver_class': 'B',
        })
        self.assertTrue(form.is_valid())

