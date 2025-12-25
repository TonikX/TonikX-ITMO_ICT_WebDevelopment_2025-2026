#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homework_board.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Создаем суперпользователя
username = 'admin'
email = 'admin@example.com'
password = 'admin123'

if User.objects.filter(username=username).exists():
    print(f'Пользователь {username} уже существует!')
    user = User.objects.get(username=username)
    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print(f'Пароль для {username} обновлен на: {password}')
else:
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Суперпользователь создан!')
    print(f'Логин: {username}')
    print(f'Пароль: {password}')

print(f'\nАдминка доступна по адресу: http://127.0.0.1:8000/admin/')

