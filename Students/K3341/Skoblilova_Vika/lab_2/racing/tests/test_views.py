"""
Тесты views приложения racing.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
from racing.models import Race, Registration, Comment


class RaceListViewTest(TestCase):
    """Тесты списка гонок."""
    
    def setUp(self):
        self.client = Client()
        Race.objects.create(
            title='Гонка 1',
            location='Москва',
            date=date.today(),
            is_published=True
        )
        Race.objects.create(
            title='Гонка 2',
            location='СПБ',
            date=date.today(),
            is_published=False
        )
    
    def test_race_list_shows_only_published(self):
        """Тест отображения только опубликованных гонок."""
        response = self.client.get(reverse('race_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Гонка 1')
        self.assertNotContains(response, 'Гонка 2')


class RegistrationViewTest(TestCase):
    """Тесты регистрации на гонку."""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.race = Race.objects.create(
            title='Гонка',
            location='Москва',
            date=date.today(),
            is_published=True
        )
    
    def test_registration_requires_login(self):
        """Тест, что регистрация требует авторизации."""
        response = self.client.post(reverse('register_for_race', args=[self.race.pk]))
        self.assertEqual(response.status_code, 302)  # Редирект на логин
        self.assertIn('login', response.url)
    
    def test_user_can_register(self):
        """Тест успешной регистрации."""
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('register_for_race', args=[self.race.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Registration.objects.filter(
                driver=self.user.driver_profile,
                race=self.race
            ).exists()
        )
    
    def test_user_cannot_edit_others_registration(self):
        """Тест, что пользователь не может редактировать чужую регистрацию."""
        user2 = User.objects.create_user(username='user2', password='12345')
        reg = Registration.objects.create(
            driver=user2.driver_profile,
            race=self.race
        )
        
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('registration_update', args=[reg.pk]))
        self.assertEqual(response.status_code, 403)  # Forbidden


class CommentViewTest(TestCase):
    """Тесты комментариев."""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.race = Race.objects.create(
            title='Гонка',
            location='Москва',
            date=date.today(),
            is_published=True
        )
    
    def test_comment_requires_login(self):
        """Тест, что комментарий требует авторизации."""
        response = self.client.post(reverse('add_comment', args=[self.race.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)
    
    def test_user_can_add_comment(self):
        """Тест добавления комментария."""
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('add_comment', args=[self.race.pk]), {
            'heat_date': date.today(),
            'kind': 'race',
            'rating': 8,
            'text': 'Отличная гонка!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Comment.objects.filter(
                race=self.race,
                author=self.user
            ).exists()
        )
    
    def test_user_cannot_edit_others_comment(self):
        """Тест, что пользователь не может редактировать чужой комментарий."""
        user2 = User.objects.create_user(username='user2', password='12345')
        comment = Comment.objects.create(
            race=self.race,
            author=user2,
            heat_date=date.today(),
            kind='race',
            rating=7,
            text='Комментарий'
        )
        
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('comment_update', args=[comment.pk]))
        self.assertEqual(response.status_code, 403)


class RaceDetailViewTest(TestCase):
    """Тесты детальной страницы гонки."""
    
    def setUp(self):
        self.client = Client()
        self.race = Race.objects.create(
            title='Гонка',
            location='Москва',
            date=date.today(),
            is_published=True
        )
    
    def test_race_detail_displays_heats_table(self):
        """Тест отображения таблицы заездов."""
        from racing.models import Heat
        from django.utils import timezone
        
        Heat.objects.create(
            race=self.race,
            start_time=timezone.now(),
            result_time_ms=120000
        )
        
        response = self.client.get(reverse('race_detail', args=[self.race.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '120000')
    
    def test_race_detail_sorting(self):
        """Тест сортировки заездов."""
        response = self.client.get(reverse('race_detail', args=[self.race.pk]) + '?sort=result_time_ms')
        self.assertEqual(response.status_code, 200)

