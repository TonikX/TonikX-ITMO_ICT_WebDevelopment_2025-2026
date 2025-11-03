# Быстрый старт - Лабораторная №3

Пошаговая инструкция для запуска системы управления читальным залом.

## Предварительные требования

- **Python** 3.10 или выше
- **pip** (менеджер пакетов Python)
- **Git** (опционально)
- **SQLite** (встроен в Python)

## Установка

### Шаг 1: Клонирование/Переход в проект

```bash
cd students/k3340/Meshcheryakov_Daniil/lab3
```

### Шаг 2: Создание виртуального окружения

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Шаг 3: Установка зависимостей

```bash
pip install -r requirements.txt
```

**Основные зависимости:**
```
Django==5.1.1
djangorestframework==3.15.2
djoser==2.2.3
djangorestframework-simplejwt==5.3.0
drf-spectacular==0.27.2
django-cors-headers==4.3.0
```

### Шаг 4: Применение миграций

```bash
python manage.py migrate
```

**Вывод:**
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, reading_room, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying reading_room.0001_initial... OK
  ...
```

### Шаг 5: Создание суперпользователя

```bash
python manage.py createsuperuser
```

**Введите данные:**
```
Username: admin
Email: admin@example.com
Password: admin123
Password (again): admin123
```

### Шаг 6: Запуск backend сервера

```bash
python manage.py runserver
```

**Вывод:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

Backend запущен на `http://localhost:8000` ✅

---

## Тестирование API

### Через Swagger UI (Рекомендуется!)

Откройте в браузере:

```
http://localhost:8000/api/schema/swagger-ui/
```

**Преимущества:**
- ✅ Интерактивное тестирование
- ✅ Авторизация через интерфейс
- ✅ Примеры запросов/ответов
- ✅ Автодокументация

**Как использовать:**

1. Найдите endpoint `/api/auth/jwt/create/`
2. Нажмите "Try it out"
3. Введите:
   ```json
   {
     "username": "admin",
     "password": "admin123"
   }
   ```
4. Нажмите "Execute"
5. Скопируйте `access` токен из ответа
6. Нажмите кнопку **"Authorize"** вверху страницы
7. Введите: `Bearer <ваш_токен>`
8. Теперь можете тестировать все endpoints! 🎉

### Через Django Admin

```
http://localhost:8000/admin/
```

Войдите с учетными данными суперпользователя.

---

## Создание тестовых данных

### Через Django Shell

```bash
python manage.py shell
```

```python
from reading_room.models import ReadingRoom, Reader, Reservation, Librarian, Schedule
from datetime import datetime, timedelta

# Создаем читальные залы
room1 = ReadingRoom.objects.create(
    number=101,
    floor=1,
    room_type='small',
    capacity=20,
    hourly_rate=150.00,
    description='Тихий малый зал для индивидуальной работы'
)

room2 = ReadingRoom.objects.create(
    number=201,
    floor=2,
    room_type='large',
    capacity=50,
    hourly_rate=300.00,
    description='Большой зал для групповых занятий'
)

# Создаем читателя
reader = Reader.objects.create(
    library_card='RD2024001',
    last_name='Иванов',
    first_name='Иван',
    patronymic='Иванович',
    phone='+79991234567',
    email='ivanov@example.com'
)

# Создаем бронирование
reservation = Reservation.objects.create(
    reader=reader,
    reading_room=room1,
    reserved_from=datetime.now(),
    reserved_to=datetime.now() + timedelta(hours=2),
    is_active=True
)

# Создаем библиотекаря
librarian = Librarian.objects.create(
    last_name='Петрова',
    first_name='Мария',
    patronymic='Сергеевна',
    is_active=True
)

# Создаем расписание
schedule = Schedule.objects.create(
    librarian=librarian,
    weekday=1,  # Понедельник
    floor=1
)

print("Тестовые данные созданы! ✅")
```

### Через Python скрипт

Создайте файл `load_test_data.py`:

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from reading_room.models import ReadingRoom, Reader, Reservation, Librarian, Schedule
from datetime import datetime, timedelta

def load_data():
    # Залы
    rooms_data = [
        {'number': 101, 'floor': 1, 'room_type': 'small', 'capacity': 20, 'hourly_rate': 150.00},
        {'number': 102, 'floor': 1, 'room_type': 'small', 'capacity': 20, 'hourly_rate': 150.00},
        {'number': 201, 'floor': 2, 'room_type': 'medium', 'capacity': 35, 'hourly_rate': 200.00},
        {'number': 301, 'floor': 3, 'room_type': 'large', 'capacity': 50, 'hourly_rate': 300.00},
    ]
    
    for data in rooms_data:
        ReadingRoom.objects.get_or_create(**data)
    
    # Читатели
    readers_data = [
        {'library_card': 'RD2024001', 'last_name': 'Иванов', 'first_name': 'Иван', 'phone': '+79991234567'},
        {'library_card': 'RD2024002', 'last_name': 'Петров', 'first_name': 'Петр', 'phone': '+79997654321'},
        {'library_card': 'RD2024003', 'last_name': 'Сидоров', 'first_name': 'Сидор', 'phone': '+79995556677'},
    ]
    
    for data in readers_data:
        Reader.objects.get_or_create(**data)
    
    # Библиотекари
    librarians_data = [
        {'last_name': 'Петрова', 'first_name': 'Мария', 'is_active': True},
        {'last_name': 'Сидорова', 'first_name': 'Анна', 'is_active': True},
    ]
    
    for data in librarians_data:
        Librarian.objects.get_or_create(**data)
    
    print("✅ Тестовые данные загружены!")
    print(f"Залов: {ReadingRoom.objects.count()}")
    print(f"Читателей: {Reader.objects.count()}")
    print(f"Библиотекарей: {Librarian.objects.count()}")

if __name__ == '__main__':
    load_data()
```

Запустите:
```bash
python load_test_data.py
```

---

## Примеры API запросов

### Регистрация пользователя

```bash
curl -X POST http://localhost:8000/api/auth/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "re_password": "testpass123"
  }'
```

### Получение JWT токена

```bash
curl -X POST http://localhost:8000/api/auth/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

**Ответ:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1Q...",
  "access": "eyJ0eXAiOiJKV1Q..."
}
```

### Список читальных залов

```bash
curl http://localhost:8000/api/reading-rooms/ \
  -H "Authorization: Bearer <your_access_token>"
```

### Создание читательского зала

```bash
curl -X POST http://localhost:8000/api/reading-rooms/ \
  -H "Authorization: Bearer <your_access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "number": 401,
    "floor": 4,
    "room_type": "medium",
    "capacity": 30,
    "hourly_rate": "180.00",
    "description": "Зал с видом на парк"
  }'
```

### Поиск свободных залов

```bash
curl "http://localhost:8000/api/reading-rooms/free/?on=2024-11-05T14:00:00" \
  -H "Authorization: Bearer <your_access_token>"
```

### Квартальный отчет

```bash
curl "http://localhost:8000/api/reports/quarter/?quarter=1" \
  -H "Authorization: Bearer <your_access_token>"
```

---

## Запуск фронтенда (Vue.js)

### В новом терминале:

```bash
cd frontend
npm install
npm run dev
```

**Вывод:**
```
VITE v5.0.0  ready in 500 ms

➜  Local:   http://localhost:3000/
➜  Network: use --host to expose
```

Фронтенд запущен на `http://localhost:3000` ✅

**Теперь откройте браузер:**
```
http://localhost:3000
```

---

## Полезные команды

### Django

```bash
# Проверка проекта
python manage.py check

# Создание миграций
python manage.py makemigrations

# Применение миграций
python manage.py migrate

# Показать миграции
python manage.py showmigrations

# Django shell
python manage.py shell

# Создать приложение
python manage.py startapp app_name

# Собрать статику
python manage.py collectstatic

# Дамп данных
python manage.py dumpdata > data.json

# Загрузить дамп
python manage.py loaddata data.json
```

### Тестирование

```bash
# Запустить все тесты
python manage.py test

# Тесты конкретного приложения
python manage.py test reading_room

# С подробным выводом
python manage.py test --verbosity=2
```

### Зависимости

```bash
# Обновить requirements.txt
pip freeze > requirements.txt

# Установить из requirements.txt
pip install -r requirements.txt

# Обновить все пакеты
pip list --outdated
pip install --upgrade <package_name>
```

---

## Проверка установки

### Шаг 1: Backend API

```bash
curl http://localhost:8000/api/
```

**Ожидаемый ответ:** JSON с доступными endpoints

### Шаг 2: Swagger UI

Откройте `http://localhost:8000/api/schema/swagger-ui/`

**Ожидается:** Интерактивная документация API

### Шаг 3: Admin Panel

Откройте `http://localhost:8000/admin/`

**Ожидается:** Страница входа в админку

### Шаг 4: Frontend

Откройте `http://localhost:3000`

**Ожидается:** Страница входа в систему

---

## Возможные проблемы и решения

### ❌ Проблема: ModuleNotFoundError

**Ошибка:**
```
ModuleNotFoundError: No module named 'rest_framework'
```

**Решение:**
```bash
pip install -r requirements.txt
```

---

### ❌ Проблема: Port already in use

**Ошибка:**
```
Error: That port is already in use.
```

**Решение:**
```bash
# Использовать другой порт
python manage.py runserver 8001
```

---

### ❌ Проблема: No migrations to apply

**Ошибка:**
```
No changes detected
```

**Решение:**
```bash
python manage.py makemigrations reading_room
python manage.py migrate
```

---

### ❌ Проблема: CORS errors

**Ошибка в консоли браузера:**
```
Access to XMLHttpRequest blocked by CORS policy
```

**Решение:** Проверьте `config/settings.py`:

```python
INSTALLED_APPS = [
    ...
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
```

---

## Следующие шаги

1. ✅ Backend запущен
2. ✅ Frontend запущен
3. 📖 [Изучите API Endpoints](api.md)
4. 🔐 [Настройте аутентификацию](auth.md)
5. 🧪 [Протестируйте систему](testing.md)
6. 🎨 [Изучите фронтенд (Lab 4)](../lab4/index.md)

---

## Справка

### Структура проекта

```
lab3/
├── config/              # Django настройки
├── reading_room/        # Основное приложение
├── frontend/            # Vue.js фронтенд
├── db.sqlite3           # База данных
├── manage.py            # Django CLI
└── requirements.txt     # Python зависимости
```

### Полезные ссылки

- **Backend API:** http://localhost:8000/api/
- **Swagger UI:** http://localhost:8000/api/schema/swagger-ui/
- **Admin:** http://localhost:8000/admin/
- **Frontend:** http://localhost:3000/

### Контакты

**Студент:** Мещеряков Даниил  
**Группа:** K3340
