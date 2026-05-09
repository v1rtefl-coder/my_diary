from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
from .models import DiaryEntry

User = get_user_model()


class DiaryEntryModelTest(TestCase):
    """Тесты для модели записей дневника"""

    def setUp(self):
        """Создаём тестового пользователя перед каждым тестом"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )

    def test_create_diary_entry(self):
        """Тест: создание записи дневника"""
        entry = DiaryEntry.objects.create(
            author=self.user,
            date=date.today(),
            morning_gratitude="Благодарен за тестирование",
            morning_affirmation="Я тестирую успешно",
            morning_goals="Написать тесты"
        )

        self.assertEqual(entry.author.username, 'testuser')
        self.assertEqual(entry.morning_gratitude, "Благодарен за тестирование")
        self.assertTrue(entry.get_morning_completed())

    def test_unique_entry_per_day(self):
        """Тест: только одна запись в день"""
        DiaryEntry.objects.create(
            author=self.user,
            date=date.today(),
            morning_gratitude="Первая запись"
        )

        # Пытаемся создать вторую запись за тот же день
        with self.assertRaises(Exception):
            DiaryEntry.objects.create(
                author=self.user,
                date=date.today(),
                morning_gratitude="Вторая запись"
            )

    def test_morning_completed_status(self):
        """Тест: проверка статуса утренней части"""
        entry = DiaryEntry.objects.create(author=self.user)

        # Изначально не заполнено
        self.assertFalse(entry.get_morning_completed())

        # Заполняем утреннюю часть
        entry.morning_gratitude = "Благодарен"
        entry.morning_affirmation = "Аффирмация"
        entry.morning_goals = "Цели"
        entry.save()

        # Теперь должно быть заполнено
        self.assertTrue(entry.get_morning_completed())

    def test_evening_completed_status(self):
        """Тест: проверка статуса вечерней части"""
        entry = DiaryEntry.objects.create(author=self.user)

        self.assertFalse(entry.get_evening_completed())

        entry.evening_wins = "Победы"
        entry.evening_improvement = "Улучшения"
        entry.evening_lesson = "Уроки"
        entry.save()

        self.assertTrue(entry.get_evening_completed())

    def test_string_representation(self):
        """Тест: строковое представление записи"""
        entry = DiaryEntry.objects.create(
            author=self.user,
            date=date.today()
        )
        self.assertEqual(str(entry), f"Дневник успеха - {date.today()}")


class UserModelTest(TestCase):
    """Тесты для модели пользователя"""

    def test_create_user(self):
        """Тест: создание обычного пользователя"""
        user = User.objects.create_user(
            username='newuser',
            password='pass123',
            email='new@example.com'
        )
        self.assertEqual(user.username, 'newuser')
        self.assertTrue(user.check_password('pass123'))
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        """Тест: создание суперпользователя"""
        admin = User.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@example.com'
        )
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)


class DiaryEntryAPITest(TestCase):
    """Тесты для API записей"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='apiuser',
            password='apipass123',
            email='api@example.com'
        )

        # Получаем JWT токен
        from rest_framework_simplejwt.tokens import RefreshToken
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        self.auth_header = f'Bearer {self.access_token}'

    def test_create_entry_via_api(self):
        """Тест: создание записи через API"""
        from django.test import Client
        client = Client()

        response = client.post(
            '/api/entries/',
            {
                'morning_gratitude': 'Тестовая благодарность',
                'morning_affirmation': 'Тестовая аффирмация',
                'morning_goals': 'Тестовые цели'
            },
            content_type='application/json',
            HTTP_AUTHORIZATION=self.auth_header
        )

        self.assertEqual(response.status_code, 201)

    def test_get_entries_list(self):
        """Тест: получение списка записей"""
        from django.test import Client
        client = Client()

        # Создаём тестовую запись
        DiaryEntry.objects.create(
            author=self.user,
            date=date.today(),
            morning_gratitude="Тест"
        )

        response = client.get(
            '/api/entries/',
            HTTP_AUTHORIZATION=self.auth_header
        )

        self.assertEqual(response.status_code, 200)