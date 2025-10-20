#!/bin/bash

echo "🏨 Hotel Management System - Quick Start"
echo "========================================"

# Проверяем наличие Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден. Установите Python3 для продолжения."
    exit 1
fi

# Проверяем наличие Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js не найден. Установите Node.js для продолжения."
    exit 1
fi

echo "✅ Python3 и Node.js найдены"

# Устанавливаем Python зависимости
echo "📦 Установка Python зависимостей..."
pip install -r requirements.txt

# Создаем миграции и применяем их
echo "🗄️ Настройка базы данных..."
python manage.py makemigrations
python manage.py migrate

# Загружаем тестовые данные
echo "📊 Загрузка тестовых данных..."
python manage.py loaddata hotel/fixtures/initial_data.json

# Создаем суперпользователя (если не существует)
echo "👤 Создание администратора..."
python manage.py shell << EOF
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('Создан пользователь admin с паролем admin')
else:
    print('Пользователь admin уже существует')
EOF

# Устанавливаем зависимости фронтенда
echo "📦 Установка зависимостей фронтенда..."
cd frontend
npm install

echo ""
echo "🎉 Установка завершена!"
echo ""
echo "Для запуска системы выполните:"
echo "1. Backend: python manage.py runserver"
echo "2. Frontend: cd frontend && npm start"
echo ""
echo "Доступ к системе:"
echo "- Frontend: http://localhost:3000"
echo "- Backend API: http://localhost:8000/api/"
echo "- Swagger UI: http://localhost:8000/api/schema/swagger-ui/"
echo "- Admin Panel: http://localhost:8000/admin/"
echo ""
echo "Тестовые данные:"
echo "- Логин: admin"
echo "- Пароль: admin"
echo ""
