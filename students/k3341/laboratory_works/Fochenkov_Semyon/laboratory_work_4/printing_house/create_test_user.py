#!/usr/bin/env python
"""
Скрипт для создания тестового пользователя
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'printing_house.settings')
django.setup()

from django.contrib.auth.models import User


def create_test_user():
    """Создание тестового пользователя"""
    username = 'testuser'
    password = 'password123'
    email = 'test@example.com'
    
    # Проверяем, существует ли пользователь
    if User.objects.filter(username=username).exists():
        print(f"Пользователь '{username}' уже существует!")
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        print(f"Пароль для пользователя '{username}' обновлен на '{password}'")
    else:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        print(f"Пользователь '{username}' успешно создан!")
        print(f"Имя пользователя: {username}")
        print(f"Пароль: {password}")
    
    print("\nТеперь вы можете войти в систему используя эти данные.")


if __name__ == '__main__':
    create_test_user()
