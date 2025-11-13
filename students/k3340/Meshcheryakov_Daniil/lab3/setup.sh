#!/bin/bash

echo "Reading Room Management System - Quick Start"
echo "==============================================="

if ! command -v python3 &> /dev/null; then
    echo "Python не найден. Установите Python для продолжения."
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "Node.js не найден. Установите Node.js для продолжения."
    exit 1
fi

echo "Python и Node.js найдены"

echo "📦 Установка Python зависимостей..."
pip install -r requirements.txt

echo "Настройка базы данных..."
python manage.py makemigrations reading_room
python manage.py migrate

echo "Загрузка тестовых данных..."
if [ -f "reading_room/fixtures/initial_data.json" ]; then
    python manage.py loaddata reading_room/fixtures/initial_data.json || echo "⚠️ Тестовые данные не загружены (возможно, требуется обновление под новую структуру)"
else
    echo "Файл с тестовыми данными не найден"
fi

echo "Создание администратора..."
python manage.py shell << EOF
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('Создан пользователь admin с паролем admin')
else:
    print('Пользователь admin уже существует')
EOF

echo "Установка зависимостей фронта..."
cd frontend
npm install
cd ..

echo ""
echo "Установка завершена!"
echo ""
echo "Для запуска системы выполните:"
echo "1. Backend: python manage.py runserver"
echo "2. Frontend: cd frontend && npm run dev"
echo ""
echo "Доступ к системе йооу:"
echo "- Frontend: http://localhost:3000"
echo "- Backend API: http://localhost:8000/api/"
echo "- Swagger UI: http://localhost:8000/api/schema/swagger-ui/"
echo "- Admin Panel: http://localhost:8000/admin/"
echo ""
echo "Тестовые данные:"
echo "- Логин: admin"
echo "- Пароль: admin"
echo ""
