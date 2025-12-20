# Эндпоинты для компании-авиаперевозчика

Base URL: `http://127.0.0.1:8000/api/`

Эта документация описывает доступные эндпоинты, методы, ожидаемые параметры и примеры запросов/ответов.

---

## Содержание
- Authentication
- Resources
  - AirlineCompany (компании)
  - Plane (самолёты)
  - Crew (экипажи)
  - CrewMember (члены экипажа)
  - Route (маршруты)
  - Flight (рейсы)
  - TransitLanding (транзитные посадки)
- Analytical / utility endpoints
- auth-demo (веб-форма с демонстрацией авторизации)
- Примечания по сериализации и ограничения

---

## Authentication

Djoser подключён по пути `/api/auth/`. Обычные Djoser endpoints включают, например:

- POST `/api/auth/users/` — регистрация пользователя
- POST `/api/auth/token/` — получить токен (авторизация через токен)
- POST `/api/auth/token/logout/` — разлогин (удалить токен)
- GET `/api/auth/users/me/` — информация о текущем пользователе

Чтобы вызвать защищённые endpoints, передавайте заголовок:
Authorization: Token <your-token>

---

## Пути, зарегистрированные в DefaultRouter

Все ресурсы доступны под префиксом `/api/`. Для каждой модели доступен стандартный набор методов ModelViewSet:

- GET /resource/ — list
- POST /resource/ — create
- GET /resource/{id}/ — retrieve
- PUT /resource/{id}/ — update
- PATCH /resource/{id}/ — partial_update
- DELETE /resource/{id}/ — destroy

Ниже — подробности и особенности.

---

### AirlineCompany — `/api/airline-companies/`

Serializer по умолчанию: `AirlineCompanySerializer` (все поля модели).
Retrieve использует: `AirlineCompanyAndPlanesAndCrewMembersSerializer` (вложенные самолёты и crew_members).

- GET /api/airline-companies/  
  Описание: список компаний. Возвращает стандартные поля модели AirlineCompany (`AirlineCompanySerializer`).

- POST /api/airline-companies/  
  Создание компании: тело запроса — поля модели (например `{"name": "My Airline"}`).

- GET /api/airline-companies/{id}/  
  Детальная информация: возвращает поля компании + вложенные:
  - `planes` — список самолётов этой компании (через обратную связь `plane_set`),
  - `crew_members` — список `CrewMember`, которые связаны с компанией (`related_name='crew_members'`).

Пример ответа (retrieve):
{
  "id": 1,
  "name": "Example Air",
  "planes": [
    { "id": 1, "number": "RA-0001", "type": "Boeing 737", "seats_capacity": 180, ... }
  ],
  "crew_members": [
    { "id": 1, "full_name": "Иванов И.И.", "position": "commander", ... }
  ]
}

---

### Plane — `/api/planes/`

Serializer по умолчанию: `PlaneSerializer`.  
Retrieve использует: `PlaneWithFlightsSerializer` — добавляет `flights` (вложенные рейсы).

- GET /api/planes/  
  Список самолётов (поля модели).

- GET /api/planes/{id}/  
  Детально: кроме полей самолёта возвращает:
  - `airline_company` — компания-авиаперевозчик (вложенный объект),
  - `flights` — список рейсов, обслуживаемых этим самолётом (используется `flight_set`).

Пример ответа (retrieve):
{
  "id": 1,
  "number": "RA-0001",
  "type": "B737",
  "seats_capacity": 180,
  "flight_speed": 800,
  "in_repair": false,
  "airline_company": { "id": 1, "name": "Example Air" },
  "flights": [
    { "id": 5, "flight_number": 123, "route": { "id": 2, "departure_point": "...", ... }, "departure_datetime": "...", "arrival_datetime": "...", "sold_tickets": 120 }
  ]
}

Замечание: сериалайзер и queryset используют `select_related('airline_company')` и `prefetch_related('flight_set__route')` для предотвращения N+1.

---

### Crew — `/api/crews/`

Serializer по умолчанию: `CrewSerializer`.  
Retrieve использует: `CrewAndMembersSerializer` — добавляет вложенные данные членов экипажа.

`CrewAndMembersSerializer`:
- `members` — read-only, вложенные `CrewMemberSerializer`

- GET /api/crews/  
  Список экипажей. Каждый объект содержит `members` (список членов экипажа).

- POST /api/crews/  
  Пример тела:
  {
    "member_ids": [1, 2, 5]
  }
  — создаёт Crew и связывает членов экипажа с указанными PK.

- GET /api/crews/{id}/  
  Возвращает объект Crew с полем `members` — развернутыми данными членов экипажа.

Замечание: в ViewSet реализованы create/update, которые применяют `instance.members.set(...)` после сохранения.

---

### CrewMember — `/api/crew-members/`

Serializer: `CrewMemberSerializer` (все поля модели).

- GET /api/crew-members/  
- POST /api/crew-members/  
- GET /api/crew-members/{id}/  
- PUT/PATCH /api/crew-members/{id}/  
- DELETE /api/crew-members/{id}/

---

### Route — `/api/routes/`

Serializer по умолчанию: `RouteSerializer`.  
Retrieve использует: `RouteWithFlightsSerializer` — добавляет `flights` (вложенные рейсы).

- GET /api/routes/  
- GET /api/routes/{id}/  
  В ответе на retrieve поле `flights` — массив рейсов, связанных с маршрутом.

Пример (retrieve):
{
  "id": 2,
  "departure_point": "MOW",
  "destination_point": "LED",
  "distance": 700,
  "landing_points": "...",
  "transit_landings": "...",
  "flights": [
    { "id": 5, "flight_number": 123, "departure_datetime": "...", "arrival_datetime": "...", "plane": { ... } }
  ]
}

---

### Flight — `/api/flights/`

Serializer по умолчанию: `FlightSerializer` (поля модели).  
Retrieve использует: `FlightWithTransitLandingsSerializer` — добавляет `transitlandings` (вложенные транзитные посадки).

- GET /api/flights/  
  Список рейсов.

- POST /api/flights/  
  Пример тела (ModelSerializer по умолчанию инклудит ManyToMany поле `crew` как список PK):
  {
    "flight_number": 555,
    "route": 2,
    "departure_datetime": "2025-11-01T10:00:00Z",
    "arrival_datetime": "2025-11-01T13:00:00Z",
    "sold_tickets": 50,
    "plane": 3,
    "crew": [1, 2]    // список PK экипажей
  }

- GET /api/flights/{id}/  
  ДЕТАЛЬНЫЙ вывод использует `FlightWithTransitLandingsSerializer` и возвращает:
  - `transitlandings` — список транзитных посадок (`landing_datetime`, `takeoff_datetime`, `landing_point`)

Пример (retrieve):
{
  "id": 5,
  "flight_number": 123,
  "route": 2,
  "departure_datetime": "2025-10-27T08:00:00Z",
  "arrival_datetime": "2025-10-27T11:00:00Z",
  "sold_tickets": 120,
  "transitlandings": [
    { "id": 10, "landing_point": "KZN", "landing_datetime": "...", "takeoff_datetime": "..." }
  ]
}

---

### TransitLanding — `/api/transit-landings/`

Serializer: `TransitLandingSerializer` (все поля модели).

- GET /api/transit-landings/  
- POST /api/transit-landings/  
- GET /api/transit-landings/{id}/  
- PUT/PATCH /api/transit-landings/{id}/  
- DELETE /api/transit-landings/{id}/

---

### Эндпоинты по заданию варианта

1) Most popular plane type for a route

- GET `/api/most_popular_plane_type/{route_id}/`

  Возвращает тип самолёта, который чаще всего используется на маршруте:
  Response:
  {
    "plane_type": "Boeing 737",
    "flight_count": 12
  }

  Если рейсов нет — 404 с сообщением.

2) Routes below capacity

- GET `/api/routes_below_capacity/{str:percentage}/`  
  Возвращает маршруты, по которым средняя заполненность рейсов < XX%.
  Response:
  {
    "under_capacity_routes": [ ... serialized routes ... ]
  }
  Ошибка при неверном проценте -> 400.

3) Available seats

- GET `/api/available_seats/{int:flight_id}/`  
  Возвращает число доступных мест на рейсе:
  {
    "available_seats": 60
  }
  404, если рейс не найден.

4) Planes under repair (требуется аутентификация)

- GET `/api/planes_under_repair/`  
  Возвращает:
  {
    "planes_under_repair": 3
  }

5) Total employees for company (требуется аутентификация)

- GET `/api/total_employees/{company_id}/`  
  Возвращает количество `CrewMember`, связанных с данной `AirlineCompany`:
  {
    "total_employees": 42
  }
  404 если компания не найдена.

---

## auth-demo (веб-форма)

- GET/POST `/api/auth-demo/` — страница/форма демонстрации логина через Django sessions + токен.
  Поведение (POST, параметр `action`):
  - `login` — аутентификация username/password, сохраняет token в `request.session['auth_token']`
  - `me` — показывает инфо о текущем пользователе (либо по сессии, либо по токену в сессии)
  - `logout` — удаляет токен и выходит из сессии

---

