from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class RegistrationTestCase(TestCase):
    def test_registration(self):
        # Подготовка данных
        data = {
            'email': 'testuser@user.com',
            'password1': 'securepassword',
            'password2': 'securepassword',
        }

        # Отправляем POST-запрос на страницу регистрации
        # self.client предоставляет способ имитировать запросы пользователя к приложению
        # reverse позволяет получить URL по имени URL-шаблона
        response = self.client.post(reverse('registration'), data)

        # Проверяем, что регистрация прошла успешно и пользователь перенаправлен на страницу входа
        # В HTTP, код 302 обычно указывает на то, что произошло перенаправление
        self.assertEqual(response.status_code, 302)
        # Здесь мы проверяем базу данных на наличие пользователя с именем 'testuser'
        self.assertTrue(User.objects.filter(email='testuser@user.com').exists())

    def test_registration_with_existing_username(self):
        # Создание пользователя
        User.objects.create_user(username='existinguser@user.com', email='existinguser@user.com', password='testpassword')

        # Попытка регистрации нового пользователя с тем же именем
        data = {
            'email': 'existinguser@user.com',
            'password1': 'anotherpassword',
            'password2': 'anotherpassword'
        }
        response = self.client.post(reverse('registration'), data)

        # Проверяем, что регистрация не прошла успешно
        self.assertNotEqual(response.status_code, 302)  # 302 — редирект, что может означать успешную регистрацию
        self.assertTrue('This email is already registered.' in response.content.decode())


class LoginTestCase(TestCase):
    def setUp(self):
        # Создаем пользователя для теста
        self.user = User.objects.create_user(username='testuser@user.com', email='testuser@user.com',
                                             password='securepassword')

    def test_login(self):
        # Подготовка данных
        data = {
            'email': 'testuser@user.com',
            'password': 'securepassword',
        }

        # Отправляем POST-запрос на страницу входа
        response = self.client.post(reverse('login'), data)

        # Проверяем, что вход прошел успешно
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_with_wrong_password(self):
        # Создание пользователя происходит в методе setUp

        # Попытка входа с неверным паролем
        data = {
            'email': 'testuser@user.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('login'), data)

        # Проверяем, что вход не прошел успешно
        self.assertNotEqual(response.status_code, 302)  # 302 — редирект, что может означать успешный вход
        self.assertTrue(
            'Invalid email or password.' in response.content.decode())


