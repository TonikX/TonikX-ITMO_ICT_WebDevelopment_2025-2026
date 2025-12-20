# Эндпоинты для компании-авиаперевозчика frontend

Base URL: `http://127.0.0.1:8000/api/`

## Authentication

### POST /register

Регистрация нового пользователя.

Request Body:
```text
{
  "username": "string",
  "password": "string",
  "email": "string"
}
```

### POST /login

Авторизация пользователя и получение токена.

Request Body:
```text
{
  "username": "string",
  "password": "string"
}
```

### POST /auth/logout/

Выход из системы (требуется токен).

### GET /profile

Получение профиля пользователя. (Требуется токен)

### PUT auth/updateProfile

Обновление данных пользователя.

Request Body:
```text
{
  "username": "string",
  "password": "string",
  "email": "string"
}
```

## Airline Companies

### GET /airlines

Получить список всех авиакомпаний.
Отображает поля модели AirlineCompany, относящиеся к каждой из них самолеты и работники.

### POST /create-company

Создать новую авиакомпанию (требуется авторизация).

Request Body:
```text
{
    "name": "string",
}
```

### PUT /edit-company/:id

Обновить данные авиакомпании (требуется авторизация).

Request Body:
```text
{
    "name": "string",
}
```

### DELETE /api/airline-companies/companyId/

Удалить авиакомпанию (требуется авторизация).

## Planes

### GET /planes/

Получить список всех самолетов.

### POST /create-plane/

Создать новый самолет (требуется авторизация).

Request Body:
```text
{
    "number": 12,
    "type": "string",
    "seats_capacity": 120,
    "flight_speed": 100,
    "airline_company": 1,
    "in_repair": true
}
```

### PUT /edit-plane/:id

Обновить данные самолета (требуется авторизация).

Request Body:
```text
{
    "number": 12,
    "type": "string",
    "seats_capacity": 120,
    "flight_speed": 100,
    "airline_company": 1,
    "in_repair": true
}
```

### DELETE /api/planes/planeId/

Удалить самолет (требуется авторизация).

## Routes

### GET /routes/

Получить список всех маршрутов.

### GET /route/:id

Получить детальную информацию о маршруте - вывести все связанные рейсы.

### POST /create-route

Создать новый маршрут (требуется авторизация).

Request Body:
```text
{
    "departure_point": "string",
    "destination_point": "string",
    "distance": 6474,
    "landing_points": "string",
    "transit_landings": "string"
}
```

### PUT /edit-route/:id

Обновить данные самолета (требуется авторизация).

Request Body:
```text
{
    "departure_point": "string",
    "destination_point": "string",
    "distance": 6474,
    "landing_points": "string",
    "transit_landings": "string"
}
```

### DELETE /api/routes/routeId/

Удалить маршрут (требуется авторизация).

## Flights

### GET /flights/

Получить список всех рейсов.

### GET /flight/:id/

Получить детальную информацию о рейсе - информация о маршруте, самолете, команде.

### POST /create-flight/

Создать новый рейс (требуется авторизация).

Request Body:
```text
{
    "flight_number": 1827,
    "departure_point": "string",
    "arrival_point": "string",
    "departure_datetime": "datetime-local",
    "arrival_datetime": "datetime-local",
    "sold_tickets": 87,
    "route": 1,
    "plane": 1,
    "crew": [],
    "is_transit": true
}
```

### PUT /edit-flight/:id/

Обновить данные рейса (требуется авторизация).

Request Body:
```text
{
    "flight_number": 1827,
    "departure_point": "string",
    "arrival_point": "string",
    "departure_datetime": "datetime-local",
    "arrival_datetime": "datetime-local",
    "sold_tickets": 87,
    "route": 1,
    "plane": 1,
    "crew": [],
    "is_transit": true
}
```

### DELETE /api/flights/flightId/

Удалить рейс (требуется авторизация).

## Crews

### GET /crews/

Получить список всех экипажей и их членов.

### GET /crews/:id/

Получить детальную информацию об экипаже.

### POST /create-crew/

Создать новый экипаж (требуется авторизация).

Request Body:
```text
{
    "members": []
}
```

### PUT /edit-crew/:id/

Обновить данные экипажа (требуется авторизация).

Request Body:
```text
{
    "members": []
}
```

### DELETE /api/crews/${crewId}/

Удалить экипаж (требуется авторизация).

## Crew Members

### POST /create-crew-member

Создать нового члена экипажа (требуется авторизация).

Request Body:
```text
{
    "full_name": "string",
    "age": 23,
    "education": "string",
    "work_experience": 2,
    "passport_info": "string",
    "flight_authorization": false,
    "company_id": 1,
    position: "string"
}
```

### PUT /edit-crew-member/:id/

Обновить данные члена экипажа (требуется авторизация).

Request Body:
```text
{
    "full_name": "string",
    "age": 23,
    "education": "string",
    "work_experience": 2,
    "passport_info": "string",
    "flight_authorization": false,
    "company_id": 1,
    position: "string"
}
```

## Задание по варианту

### GET /variant-task/

Получение запросов по варианту:

Задание 1: Самая популярная марка самолета на маршруте

Задание 2: Маршруты с заполненностью менее XX%

Задание 3: Наличие свободных мест на рейс

Задание 4: Количество самолетов в ремонте

Задание 5: Количество работников компании