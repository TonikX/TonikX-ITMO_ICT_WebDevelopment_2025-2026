# Printing House API

## Описание проекта

Проект Printing House представляет собой программную систему для отслеживания распределения газет по почтовым отделениям, печатающихся в типографиях города. Система обеспечивает хранение, просмотр и изменение сведений о газетах, почтовых отделениях и типографиях.

## Основные возможности

- Управление газетами (создание, редактирование, просмотр)
- Управление типографиями с отслеживанием их статуса (активна/закрыта)
- Управление почтовыми отделениями
- Отслеживание тиражей газет в типографиях
- Отслеживание распределения газет по почтовым отделениям
- Сложные запросы для получения аналитической информации
- RESTful API с использованием Django REST Framework
- Аутентификация через токены с использованием Djoser

## Технологии

- Django 4.2.7
- Django REST Framework 3.14.0
- Djoser 2.1.0 (для аутентификации)
- SQLite (база данных)
- Python 3.8+

## Модели данных

### Газета (Newspaper)
- Название газеты
- Индекс издания (уникальный)
- ФИО редактора (имя, фамилия, отчество)
- Цена экземпляра

### Типография (PrintingHouse)
- Название типографии
- Адрес
- Статус активности (активна/закрыта)

### Почтовое отделение (PostOffice)
- Номер почтового отделения (уникальный)
- Адрес

### Тираж (PrintingRun)
- Связь типографии и газеты
- Размер тиража

### Распределение (Distribution)
- Связь почтового отделения, газеты и типографии
- Количество экземпляров

## API Endpoints

### Аутентификация

Все API endpoints требуют аутентификации через токены.

**Регистрация пользователя:**
```
POST /auth/users/
```

**Получение токена:**
```
POST /auth/token/login/
```

**Информация о текущем пользователе:**
```
GET /auth/users/me/
```

### Газеты

- `GET /api/newspapers/` - список всех газет
- `GET /api/newspapers/{id}/` - детали газеты
- `POST /api/newspapers/` - создание газеты
- `PUT /api/newspapers/{id}/` - обновление газеты
- `DELETE /api/newspapers/{id}/` - удаление газеты
- `GET /api/newspapers/{id}/full_detail/` - газета с вложенными объектами (many-to-many)
- `GET /api/newspapers/by_name/?name=...` - адреса типографий для газеты
- `GET /api/newspapers/info/?id=...` - справка об индексе и цене

### Типографии

- `GET /api/printing-houses/` - список всех типографий
- `GET /api/printing-houses/{id}/` - детали типографии
- `POST /api/printing-houses/` - создание типографии
- `PUT /api/printing-houses/{id}/` - обновление типографии
- `DELETE /api/printing-houses/{id}/` - удаление типографии
- `GET /api/printing-houses/{id}/full_detail/` - типография с вложенными тиражами (one-to-many)
- `GET /api/printing-houses/{id}/largest_circulation_editor/` - редактор газеты с самым большим тиражом
- `GET /api/printing-houses/report/` - отчет о работе типографий

### Почтовые отделения

- `GET /api/post-offices/` - список всех почтовых отделений
- `GET /api/post-offices/{id}/` - детали почтового отделения
- `POST /api/post-offices/` - создание почтового отделения
- `PUT /api/post-offices/{id}/` - обновление почтового отделения
- `DELETE /api/post-offices/{id}/` - удаление почтового отделения
- `GET /api/post-offices/{id}/full_detail/` - почтовое отделение с вложенными распределениями (one-to-many)
- `GET /api/post-offices/by_price/?min_price=...` - почтовые отделения для газет дороже указанной цены
- `GET /api/post-offices/low_quantity/?max_quantity=...` - газеты с количеством меньше заданного

### Распределения

- `GET /api/distributions/` - список всех распределений
- `GET /api/distributions/{id}/` - детали распределения
- `POST /api/distributions/` - создание распределения
- `PUT /api/distributions/{id}/` - обновление распределения
- `DELETE /api/distributions/{id}/` - удаление распределения
- `GET /api/distributions/by_newspaper_and_address/?newspaper_id=...&address=...` - куда поступает газета по адресу

## Запросы из задания

### 1. По каким адресам печатаются газеты данного наименования?

```
GET /api/newspapers/by_name/?name=Городские вести
```

### 2. Фамилия редактора газеты, которая печатается в указанной типографии самым большим тиражом

```
GET /api/printing-houses/{id}/largest_circulation_editor/
```

### 3. На какие почтовые отделения (адреса) поступает газета, имеющая цену, больше указанной

```
GET /api/post-offices/by_price/?min_price=30.00
```

### 4. Какие газеты и куда (номер почты) поступают в количестве меньшем, чем заданное

```
GET /api/post-offices/low_quantity/?max_quantity=200
```

### 5. Куда поступает данная газета, печатающаяся по данному адресу

```
GET /api/distributions/by_newspaper_and_address/?newspaper_id=1&address=Промышленная
```

### 6. Справка об индексе и цене указанной газеты

```
GET /api/newspapers/info/?id=1
или
GET /api/newspapers/info/?name=Городские вести
```

### 7. Отчет о работе типографий с почтовыми отделениями города

```
GET /api/printing-houses/report/
```

## GET-запросы с вложенными объектами

### One-to-Many (один-ко-многим)

**Типография с вложенными тиражами:**
```
GET /api/printing-houses/{id}/full_detail/
```

**Почтовое отделение с вложенными распределениями:**
```
GET /api/post-offices/{id}/full_detail/
```

### Many-to-Many (многие-ко-многим)

**Газета с вложенными тиражами и распределениями:**
```
GET /api/newspapers/{id}/full_detail/
```

## Установка и запуск

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Применение миграций

```bash
cd printing_house
python manage.py migrate
```

### 3. Создание тестовых данных

```bash
python create_newspaper_data.py
```

### 4. Запуск сервера

```bash
python manage.py runserver
```

### 5. Доступ к API

- API: http://localhost:8000/api/
- Аутентификация: http://localhost:8000/auth/
- Админ-панель: http://localhost:8000/admin/

## Примеры использования

### Получение токена

```bash
curl -X POST http://localhost:8000/auth/token/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}'
```

### Использование токена в запросах

```bash
curl -X GET http://localhost:8000/api/newspapers/ \
  -H "Authorization: Token <ваш_токен>"
```

### Получение газеты с вложенными объектами

```bash
curl -X GET http://localhost:8000/api/newspapers/1/full_detail/ \
  -H "Authorization: Token <ваш_токен>"
```

### Получение отчета по типографиям

```bash
curl -X GET http://localhost:8000/api/printing-houses/report/ \
  -H "Authorization: Token <ваш_токен>"
```

