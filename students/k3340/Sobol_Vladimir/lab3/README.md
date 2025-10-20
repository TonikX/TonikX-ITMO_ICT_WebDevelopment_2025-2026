# Hotel Management System

Система управления гостиницей с веб-интерфейсом и REST API.

## Описание

Система предназначена для администратора гостиницы и обеспечивает:
- Управление номерами (одноместные, двухместные, трехместные)
- Управление клиентами и их проживаниями
- Управление сотрудниками и их расписанием
- Генерацию отчетов по кварталам
- Поиск свободных номеров

## Технологии

### Backend
- Django 5.1.1
- Django REST Framework 3.15.2
- Djoser (аутентификация)
- drf-spectacular (Swagger документация)
- SQLite (база данных)

### Frontend
- React 18.2.0
- Ant Design 5.2.0
- React Router 6.8.0
- Axios (HTTP клиент)

## Установка и запуск

### 1. Установка зависимостей

```bash
# Backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### 2. Настройка базы данных

```bash
# Создание миграций
python manage.py makemigrations

# Применение миграций
python manage.py migrate

# Загрузка тестовых данных
python manage.py loaddata hotel/fixtures/initial_data.json

# Создание суперпользователя
python manage.py createsuperuser
```

### 3. Запуск

```bash
# Backend (терминал 1)
python manage.py runserver

# Frontend (терминал 2)
cd frontend
npm start
```

## Доступ к системе

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Swagger UI**: http://localhost:8000/api/schema/swagger-ui/
- **Admin Panel**: http://localhost:8000/admin/

## Тестовые данные

Система поставляется с тестовыми данными:
- 5 номеров разных типов
- 4 клиента из разных городов
- 3 сотрудника (2 активных, 1 неактивный)
- Расписание работы сотрудников
- Примеры проживаний

## API Endpoints

### Аутентификация
- `POST /api/auth/token/login/` - Вход
- `POST /api/auth/token/logout/` - Выход
- `GET /api/auth/users/me/` - Текущий пользователь

### Номера
- `GET /api/rooms/` - Список номеров
- `POST /api/rooms/` - Создать номер
- `GET /api/rooms/{id}/` - Детали номера
- `PUT /api/rooms/{id}/` - Обновить номер
- `DELETE /api/rooms/{id}/` - Удалить номер
- `GET /api/rooms/free/?on=YYYY-MM-DD` - Свободные номера
- `GET /api/rooms/{id}/clients/?start=YYYY-MM-DD&end=YYYY-MM-DD` - Клиенты в номере за период

### Клиенты
- `GET /api/clients/` - Список клиентов
- `POST /api/clients/` - Создать клиента
- `GET /api/clients/{id}/` - Детали клиента
- `PUT /api/clients/{id}/` - Обновить клиента
- `DELETE /api/clients/{id}/` - Удалить клиента
- `GET /api/clients/count-by-city/?city=название` - Количество клиентов по городу
- `GET /api/clients/{id}/cleaner/?weekday=1-7` - Кто убирал номер клиента
- `GET /api/clients/{id}/co-stayers/?start=YYYY-MM-DD&end=YYYY-MM-DD` - Совместно проживающие

### Проживания
- `GET /api/stays/` - Список проживаний
- `POST /api/stays/` - Создать проживание
- `GET /api/stays/{id}/` - Детали проживания
- `PUT /api/stays/{id}/` - Обновить проживание
- `DELETE /api/stays/{id}/` - Удалить проживание

### Сотрудники
- `GET /api/employees/` - Список сотрудников
- `POST /api/employees/` - Создать сотрудника
- `GET /api/employees/{id}/` - Детали сотрудника
- `PUT /api/employees/{id}/` - Обновить сотрудника
- `DELETE /api/employees/{id}/` - Удалить сотрудника
- `POST /api/employees/{id}/fire/` - Уволить сотрудника
- `POST /api/employees/{id}/hire/` - Принять на работу

### Расписание
- `GET /api/schedules/` - Список расписаний
- `POST /api/schedules/` - Создать расписание
- `GET /api/schedules/{id}/` - Детали расписания
- `PUT /api/schedules/{id}/` - Обновить расписание
- `DELETE /api/schedules/{id}/` - Удалить расписание

### Отчеты
- `GET /api/reports/quarter/?quarter=1-4` - Отчет по кварталу

## Функциональность

### Панель управления
- Общая статистика (номера, клиенты, сотрудники, доходы)
- Свободные номера на выбранную дату
- Последние проживания

### Управление номерами
- CRUD операции с номерами
- Поиск свободных номеров
- Фильтрация по типу и этажу

### Управление клиентами
- CRUD операции с клиентами
- Поиск по городу
- Информация о совместно проживающих

### Управление проживаниями
- CRUD операции с проживаниями
- Отслеживание статуса (проживает/выселен)

### Управление сотрудниками
- CRUD операции с сотрудниками
- Прием/увольнение сотрудников
- Управление расписанием

### Отчеты
- Квартальные отчеты с доходностью
- Статистика по номерам и этажам
- Анализ загруженности

## Авторизация

Система использует токенную аутентификацию Django REST Framework.
Для доступа к API необходимо получить токен через `/api/auth/token/login/`.

## Разработка

### Структура проекта
```
lab3/
├── config/                 # Настройки Django
├── hotel/                  # Основное приложение
│   ├── models.py          # Модели данных
│   ├── views.py           # API представления
│   ├── serializers.py     # Сериализаторы
│   ├── urls.py            # URL маршруты
│   └── fixtures/          # Тестовые данные
├── frontend/              # React приложение
│   ├── src/
│   │   ├── components/    # React компоненты
│   │   ├── pages/         # Страницы
│   │   └── services/      # API сервисы
│   └── package.json
└── requirements.txt       # Python зависимости
```

### Добавление новых функций
1. Обновите модели в `hotel/models.py`
2. Создайте миграции: `python manage.py makemigrations`
3. Примените миграции: `python manage.py migrate`
4. Обновите сериализаторы в `hotel/serializers.py`
5. Добавьте представления в `hotel/views.py`
6. Обновите URL маршруты в `hotel/urls.py`
7. Обновите фронтенд компоненты

## Лицензия

MIT License
