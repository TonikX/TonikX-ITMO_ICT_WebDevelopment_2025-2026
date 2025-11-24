# Документация API - КурКод (Backend)

## Базовая информация
- Базовый URL: http://localhost:8189/
- Формат: application/json; charset=UTF-8
- Аутентификация: JWT в HttpOnly Secure cookie с именем Authorization
- Swagger UI: /swagger-ui.html
- OpenAPI JSON: /v3/api-docs

---

## Аутентификация (Authentication)

**POST**: `/auth/login`

Назначение: аутентификация по email и паролю. На успех устанавливается cookie Authorization.

Тело запроса:
```json
{
  "email": "user@example.com",
  "password": "secret"
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 5,
    "username": "john",
    "email": "user@example.com",
    "registrationStatus": "ACTIVE",
    "lastLogin": "2024-01-01T12:34:56",
    "token": "<access-token>",
    "refreshToken": "<refresh-token>",
    "roles": [ { "id": 1, "name": "ROLE_USER" } ]
  },
  "success": true
}
```

**GET**: `/auth/refresh/token?token=<refreshToken>`

Назначение: получить новый access-токен по refresh-токену. На успех устанавливается новая cookie Authorization.

Параметры:
- `token` (query) - refresh токен

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 5,
    "username": "john",
    "email": "user@example.com",
    "registrationStatus": "ACTIVE",
    "lastLogin": "2024-01-01T12:34:56",
    "token": "<new-access-token>",
    "refreshToken": "<refresh-token>",
    "roles": [ { "id": 1, "name": "ROLE_USER" } ]
  },
  "success": true
}
```

**POST**: `/auth/register`

Назначение: регистрация нового пользователя и немедленная аутентификация; cookie Authorization устанавливается в ответе.

Тело запроса:
```json
{
  "username": "john",
  "email": "user@example.com",
  "password": "secret",
  "confirmPassword": "secret"
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 6,
    "username": "john",
    "email": "user@example.com",
    "registrationStatus": "ACTIVE",
    "lastLogin": "2024-01-01T12:34:56",
    "token": "<access-token>",
    "refreshToken": "<refresh-token>",
    "roles": [ { "id": 1, "name": "ROLE_USER" } ]
  },
  "success": true
}
```

---

## Пользователи (Users)

**GET**: `/api/v1/users/id/{userId}`

Назначение: получение пользователя по идентификатору.

Параметры:
- `userId` (path) - идентификатор пользователя

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 5,
    "username": "john",
    "email": "user@example.com",
    "role": { "id": 1, "name": "ROLE_USER" },
    "registrationStatus": "ACTIVE",
    "roles": [ { "id": 1, "name": "ROLE_USER" } ],
    "createdAt": "2024-01-01T10:00:00",
    "updatedAt": "2024-01-02T11:00:00",
    "version": 0
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"0"`

**GET**: `/api/v1/users/username/{username}`

Назначение: получение пользователя по имени пользователя.

Параметры:
- `username` (path) - имя пользователя

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 5,
    "username": "john",
    "email": "user@example.com",
    "role": { "id": 1, "name": "ROLE_USER" },
    "registrationStatus": "ACTIVE",
    "roles": [ { "id": 1, "name": "ROLE_USER" } ],
    "createdAt": "2024-01-01T10:00:00",
    "updatedAt": "2024-01-02T11:00:00",
    "version": 0
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"0"`

**POST**: `/api/v1/users`

Назначение: создание нового пользователя.

Тело запроса:
```json
{
  "username": "john",
  "password": "secret",
  "email": "user@example.com"
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 7,
    "username": "john",
    "email": "user@example.com",
    "role": { "id": 1, "name": "ROLE_USER" },
    "registrationStatus": "PENDING",
    "roles": [ { "id": 1, "name": "ROLE_USER" } ],
    "createdAt": "2024-01-01T10:00:00",
    "updatedAt": "2024-01-01T10:00:00",
    "version": 0
  },
  "success": true
}
```

Заголовки ответа:
- `Location`: `/api/v1/users/id/7`
- `ETag`: `"0"`

**PUT**: `/api/v1/users/{userId}`

Назначение: полная замена пользователя по идентификатору.

Параметры:
- `userId` (path) - идентификатор пользователя

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Тело запроса:
```json
{
  "username": "john",
  "password": "secret",
  "email": "user@example.com"
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 7,
    "username": "john",
    "email": "user@example.com",
    "role": { "id": 1, "name": "ROLE_USER" },
    "registrationStatus": "ACTIVE",
    "roles": [ { "id": 1, "name": "ROLE_USER" } ],
    "createdAt": "2024-01-01T10:00:00",
    "updatedAt": "2024-01-04T09:00:00",
    "version": 1
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"1"`

**PATCH**: `/api/v1/users/{userId}`

Назначение: частичное обновление пользователя по идентификатору.

Параметры:
- `userId` (path) - идентификатор пользователя

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Тело запроса (все поля опциональны):
```json
{
  "username": "johnny",
  "password": "new-secret",
  "email": "johnny@example.com"
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 7,
    "username": "johnny",
    "email": "johnny@example.com",
    "role": { "id": 1, "name": "ROLE_USER" },
    "registrationStatus": "ACTIVE",
    "roles": [ { "id": 1, "name": "ROLE_USER" } ],
    "createdAt": "2024-01-01T10:00:00",
    "updatedAt": "2024-01-03T12:00:00",
    "version": 2
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"2"`

**DELETE**: `/api/v1/users/{userId}`

Назначение: удаление пользователя по идентификатору.

Параметры:
- `userId` (path) - идентификатор пользователя

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Ответ: 204 No Content

---

## Административные операции с пользователями (Admin Users)

**PATCH**: `/api/v1/admin/users/{id}/role`

Назначение: изменение роли пользователя. Требует ETag для оптимистичной блокировки.

Параметры:
- `id` (path) - идентификатор пользователя

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Тело запроса:
```json
{
  "roleId": 2
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 10,
    "username": "john",
    "email": "user@example.com",
    "role": { "id": 2, "name": "ROLE_ADMIN" },
    "registrationStatus": "ACTIVE",
    "roles": [ { "id": 2, "name": "ROLE_ADMIN" } ],
    "createdAt": "2024-01-01T10:00:00",
    "updatedAt": "2024-01-05T10:00:00",
    "version": 1
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"1"`

**POST**: `/api/v1/admin/users/{id}/activate`

Назначение: активация пользователя (установка статуса ACTIVE). Требует ETag.

Параметры:
- `id` (path) - идентификатор пользователя

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 10,
    "username": "john",
    "email": "user@example.com",
    "role": { "id": 1, "name": "ROLE_USER" },
    "registrationStatus": "ACTIVE",
    "roles": [ { "id": 1, "name": "ROLE_USER" } ],
    "createdAt": "2024-01-01T10:00:00",
    "updatedAt": "2024-01-05T10:00:00",
    "version": 1
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"1"`

**POST**: `/api/v1/admin/users/{id}/deactivate`

Назначение: деактивация пользователя (установка статуса INACTIVE). Требует ETag.

Параметры:
- `id` (path) - идентификатор пользователя

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 10,
    "username": "john",
    "email": "user@example.com",
    "role": { "id": 1, "name": "ROLE_USER" },
    "registrationStatus": "INACTIVE",
    "roles": [ { "id": 1, "name": "ROLE_USER" } ],
    "createdAt": "2024-01-01T10:00:00",
    "updatedAt": "2024-01-05T10:00:00",
    "version": 1
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"1"`

---

## Работники (Workers)

**GET**: `/api/v1/workers`

Назначение: получение списка всех работников.

Ответ:
```json
{
  "message": "",
  "payload": [
    {
      "id": 1,
      "firstName": "Ivan",
      "lastName": "Ivanov",
      "patronymic": "Petrovich",
      "cages": [],
      "version": 0
    },
    {
      "id": 2,
      "firstName": "Petr",
      "lastName": "Petrov",
      "patronymic": null,
      "cages": [],
      "version": 0
    }
  ],
  "success": true
}
```

**GET**: `/api/v1/workers/{id}`

Назначение: получение работника по идентификатору.

Параметры:
- `id` (path) - идентификатор работника

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 1,
    "firstName": "Ivan",
    "lastName": "Ivanov",
    "patronymic": "Petrovich",
    "cages": [],
    "version": 0
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"0"`

**POST**: `/api/v1/workers`

Назначение: создание нового работника.

Тело запроса:
```json
{
  "firstName": "Ivan",
  "lastName": "Ivanov",
  "patronymic": "Petrovich"
}
```

Ответ: 201 Created
```json
{
  "message": "",
  "payload": {
    "id": 3,
    "firstName": "Ivan",
    "lastName": "Ivanov",
    "patronymic": "Petrovich",
    "cages": [],
    "version": 0
  },
  "success": true
}
```

Заголовки ответа:
- `Location`: `/api/v1/workers/3`
- `ETag`: `"0"`

**PUT**: `/api/v1/workers/{id}`

Назначение: полная замена работника по идентификатору.

Параметры:
- `id` (path) - идентификатор работника

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Тело запроса:
```json
{
  "firstName": "Ivan",
  "lastName": "Ivanov",
  "patronymic": "Petrovich"
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 1,
    "firstName": "Ivan",
    "lastName": "Ivanov",
    "patronymic": "Petrovich",
    "cages": [],
    "version": 1
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"1"`

**PATCH**: `/api/v1/workers/{id}`

Назначение: частичное обновление работника по идентификатору.

Параметры:
- `id` (path) - идентификатор работника

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Тело запроса (все поля опциональны):
```json
{
  "lastName": "Sidorov"
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 1,
    "firstName": "Ivan",
    "lastName": "Sidorov",
    "patronymic": "Petrovich",
    "cages": [],
    "version": 2
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"2"`

**DELETE**: `/api/v1/workers/{id}`

Назначение: удаление работника по идентификатору.

Параметры:
- `id` (path) - идентификатор работника

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Ответ: 204 No Content

---

## Паспорт (Passport)

**GET**: `/api/v1/workers/{workerId}/passport`

Назначение: получение паспорта работника по идентификатору работника.

Параметры:
- `workerId` (path) - идентификатор работника

Ответ:
```json
{
  "message": "",
  "payload": {
    "series": "1234",
    "number": "567890",
    "createdAt": "2024-01-01T10:00:00",
    "updatedAt": "2024-01-02T11:00:00",
    "version": 0
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"0"`

**POST**: `/api/v1/workers/{workerId}/passport`

Назначение: создание паспорта для работника. Каждый работник может иметь только один паспорт.

Параметры:
- `workerId` (path) - идентификатор работника

Тело запроса:
```json
{
  "series": "1234",
  "number": "567890"
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "series": "1234",
    "number": "567890",
    "createdAt": "2024-01-01T10:00:00",
    "updatedAt": "2024-01-01T10:00:00",
    "version": 0
  },
  "success": true
}
```

**PUT**: `/api/v1/workers/{workerId}/passport`

Назначение: полная замена паспорта работника.

Параметры:
- `workerId` (path) - идентификатор работника

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Тело запроса:
```json
{
  "series": "1234",
  "number": "567890"
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "series": "1234",
    "number": "567890",
    "createdAt": "2024-01-01T10:00:00",
    "updatedAt": "2024-01-03T12:00:00",
    "version": 1
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"1"`

**PATCH**: `/api/v1/workers/{workerId}/passport`

Назначение: частичное обновление паспорта работника.

Параметры:
- `workerId` (path) - идентификатор работника

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Тело запроса (все поля опциональны):
```json
{
  "series": "5678",
  "number": "901234"
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "series": "5678",
    "number": "901234",
    "createdAt": "2024-01-01T10:00:00",
    "updatedAt": "2024-01-03T12:00:00",
    "version": 2
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"2"`

**DELETE**: `/api/v1/workers/{workerId}/passport`

Назначение: удаление паспорта работника.

Параметры:
- `workerId` (path) - идентификатор работника

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Ответ: 204 No Content

---

## Трудовой договор (Employment Contract)

**GET**: `/api/v1/workers/{workerId}/contract`

Назначение: получение трудового договора работника по идентификатору работника.

Параметры:
- `workerId` (path) - идентификатор работника

Ответ:
```json
{
  "message": "",
  "payload": {
    "contractNumber": "CN-001",
    "salary": 50000,
    "position": "Developer",
    "firstNameWorker": "Ivan",
    "lastNameWorker": "Ivanov",
    "startDate": "2024-01-01",
    "endDate": "2025-01-01",
    "createdAt": "2024-01-01T10:00:00",
    "updatedAt": "2024-01-02T11:00:00",
    "version": 0
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"0"`

**POST**: `/api/v1/workers/{workerId}/contract`

Назначение: создание трудового договора для работника. Каждый работник может иметь только один активный договор.

Параметры:
- `workerId` (path) - идентификатор работника

Тело запроса:
```json
{
  "contractNumber": "CN-001",
  "salary": 50000,
  "position": "Developer",
  "startDate": "2024-01-01",
  "endDate": "2025-01-01"
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "contractNumber": "CN-001",
    "salary": 50000,
    "position": "Developer",
    "firstNameWorker": "Ivan",
    "lastNameWorker": "Ivanov",
    "startDate": "2024-01-01",
    "endDate": "2025-01-01",
    "createdAt": "2024-01-01T10:00:00",
    "updatedAt": "2024-01-01T10:00:00",
    "version": 0
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"0"`

**PUT**: `/api/v1/workers/{workerId}/contract`

Назначение: полная замена трудового договора работника.

Параметры:
- `workerId` (path) - идентификатор работника

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Тело запроса:
```json
{
  "contractNumber": "CN-001",
  "salary": 60000,
  "position": "Senior Developer",
  "startDate": "2024-01-01",
  "endDate": "2025-01-01"
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "contractNumber": "CN-001",
    "salary": 60000,
    "position": "Senior Developer",
    "firstNameWorker": "Ivan",
    "lastNameWorker": "Ivanov",
    "startDate": "2024-01-01",
    "endDate": "2025-01-01",
    "createdAt": "2024-01-01T10:00:00",
    "updatedAt": "2024-01-03T12:00:00",
    "version": 1
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"1"`

**PATCH**: `/api/v1/workers/{workerId}/contract`

Назначение: частичное обновление трудового договора работника.

Параметры:
- `workerId` (path) - идентификатор работника

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Тело запроса (все поля опциональны):
```json
{
  "position": "Lead Developer"
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "contractNumber": "CN-001",
    "salary": 60000,
    "position": "Lead Developer",
    "firstNameWorker": "Ivan",
    "lastNameWorker": "Ivanov",
    "startDate": "2024-01-01",
    "endDate": "2025-01-01",
    "createdAt": "2024-01-01T10:00:00",
    "updatedAt": "2024-01-03T12:00:00",
    "version": 2
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"2"`

**DELETE**: `/api/v1/workers/{workerId}/contract`

Назначение: удаление трудового договора работника.

Параметры:
- `workerId` (path) - идентификатор работника

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Ответ: 204 No Content

---

## Штат (Staff)

**GET**: `/api/v1/staff`

Назначение: получение списка всех должностей в системе.

Ответ:
```json
{
  "message": "",
  "payload": [
    {
      "id": 7,
      "position": "Manager",
      "createdAt": "2024-01-01T10:00:00",
      "updatedAt": "2024-01-01T10:00:00",
      "version": 0
    },
    {
      "id": 8,
      "position": "Developer",
      "createdAt": "2024-01-01T10:00:00",
      "updatedAt": "2024-01-01T10:00:00",
      "version": 0
    }
  ],
  "success": true
}
```

**GET**: `/api/v1/staff/{id}`

Назначение: получение должности по идентификатору.

Параметры:
- `id` (path) - идентификатор должности

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 7,
    "position": "Manager",
    "createdAt": "2024-01-01T10:00:00",
    "updatedAt": "2024-01-01T10:00:00",
    "version": 0
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"0"`

**POST**: `/api/v1/staff`

Назначение: создание новой должности. Название должно быть уникальным.

Тело запроса:
```json
{
  "position": "Manager"
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 9,
    "position": "Manager",
    "createdAt": "2024-01-01T10:00:00",
    "updatedAt": "2024-01-01T10:00:00",
    "version": 0
  },
  "success": true
}
```

Заголовки ответа:
- `Location`: `/api/v1/staff/9`
- `ETag`: `"0"`

**PUT**: `/api/v1/staff/{id}`

Назначение: полная замена должности по идентификатору.

Параметры:
- `id` (path) - идентификатор должности

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Тело запроса:
```json
{
  "position": "Senior Manager"
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 7,
    "position": "Senior Manager",
    "createdAt": "2024-01-01T10:00:00",
    "updatedAt": "2024-01-03T12:00:00",
    "version": 1
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"1"`

**PATCH**: `/api/v1/staff/{id}`

Назначение: частичное обновление должности по идентификатору.

Параметры:
- `id` (path) - идентификатор должности

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Тело запроса (все поля опциональны):
```json
{
  "position": "Lead"
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 7,
    "position": "Lead",
    "createdAt": "2024-01-01T10:00:00",
    "updatedAt": "2024-01-03T12:00:00",
    "version": 2
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"2"`

**DELETE**: `/api/v1/staff/{id}`

Назначение: удаление должности по идентификатору.

Параметры:
- `id` (path) - идентификатор должности

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Ответ: 204 No Content

---

## Цеха (Workshops)

**GET**: `/api/v1/workshops`

Назначение: получение списка всех цехов в системе.

Ответ:
```json
{
  "message": "",
  "payload": [
    {
      "id": 1,
      "workshopNumber": 1,
      "version": 0
    },
    {
      "id": 2,
      "workshopNumber": 2,
      "version": 0
    }
  ],
  "success": true
}
```

**GET**: `/api/v1/workshops/{id}`

Назначение: получение цеха по идентификатору.

Параметры:
- `id` (path) - идентификатор цеха

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 1,
    "workshopNumber": 1,
    "version": 0
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"0"`

**POST**: `/api/v1/workshops`

Назначение: создание нового цеха.

Тело запроса:
```json
{
  "workshopNumber": 3
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 3,
    "workshopNumber": 3,
    "version": 0
  },
  "success": true
}
```

Заголовки ответа:
- `Location`: `/api/v1/workshops/3`
- `ETag`: `"0"`

**PUT**: `/api/v1/workshops/{id}`

Назначение: полная замена цеха по идентификатору.

Параметры:
- `id` (path) - идентификатор цеха

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Тело запроса:
```json
{
  "workshopNumber": 4
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 1,
    "workshopNumber": 4,
    "version": 1
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"1"`

**PATCH**: `/api/v1/workshops/{id}`

Назначение: частичное обновление цеха по идентификатору.

Параметры:
- `id` (path) - идентификатор цеха

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Тело запроса (все поля опциональны):
```json
{
  "workshopNumber": 5
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 1,
    "workshopNumber": 5,
    "version": 2
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"2"`

**DELETE**: `/api/v1/workshops/{id}`

Назначение: удаление цеха по идентификатору.

Параметры:
- `id` (path) - идентификатор цеха

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Ответ: 204 No Content

---

## Ряды (Rows)

**GET**: `/api/v1/workshops/{workshopId}/rows`

Назначение: получение списка всех рядов в цехе.

Параметры:
- `workshopId` (path) - идентификатор цеха

Ответ:
```json
{
  "message": "",
  "payload": [
    {
      "id": 1,
      "rowNumber": 1,
      "workshopId": 1,
      "createdAt": "2024-01-01T10:00:00",
      "updatedAt": "2024-01-01T10:00:00",
      "version": 0
    },
    {
      "id": 2,
      "rowNumber": 2,
      "workshopId": 1,
      "createdAt": "2024-01-01T10:00:00",
      "updatedAt": "2024-01-01T10:00:00",
      "version": 0
    }
  ],
  "success": true
}
```

**GET**: `/api/v1/workshops/{workshopId}/rows/{rowNumber}`

Назначение: получение ряда по номеру в цехе.

Параметры:
- `workshopId` (path) - идентификатор цеха
- `rowNumber` (path) - номер ряда

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 1,
    "rowNumber": 1,
    "workshopId": 1,
    "createdAt": "2024-01-01T10:00:00",
    "updatedAt": "2024-01-01T10:00:00",
    "version": 0
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"0"`

**POST**: `/api/v1/workshops/{workshopId}/rows`

Назначение: создание нового ряда в цехе.

Параметры:
- `workshopId` (path) - идентификатор цеха

Тело запроса:
```json
{
  "rowNumber": 3
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 3,
    "rowNumber": 3,
    "workshopId": 1,
    "createdAt": "2024-01-01T10:00:00",
    "updatedAt": "2024-01-01T10:00:00",
    "version": 0
  },
  "success": true
}
```

Заголовки ответа:
- `Location`: `/api/v1/workshops/1/rows/3`
- `ETag`: `"0"`

**PUT**: `/api/v1/workshops/{workshopId}/rows/{rowNumber}`

Назначение: полная замена ряда по номеру в цехе.

Параметры:
- `workshopId` (path) - идентификатор цеха
- `rowNumber` (path) - номер ряда

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Тело запроса:
```json
{
  "rowNumber": 4
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 1,
    "rowNumber": 4,
    "workshopId": 1,
    "createdAt": "2024-01-01T10:00:00",
    "updatedAt": "2024-01-03T12:00:00",
    "version": 1
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"1"`

**PATCH**: `/api/v1/workshops/{workshopId}/rows/{rowNumber}`

Назначение: частичное обновление ряда по номеру в цехе.

Параметры:
- `workshopId` (path) - идентификатор цеха
- `rowNumber` (path) - номер ряда

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Тело запроса (все поля опциональны):
```json
{
  "rowNumber": 5
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 1,
    "rowNumber": 5,
    "workshopId": 1,
    "createdAt": "2024-01-01T10:00:00",
    "updatedAt": "2024-01-03T12:00:00",
    "version": 2
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"2"`

**DELETE**: `/api/v1/workshops/{workshopId}/rows/{rowNumber}`

Назначение: удаление ряда по номеру в цехе.

Параметры:
- `workshopId` (path) - идентификатор цеха
- `rowNumber` (path) - номер ряда

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Ответ: 204 No Content

---

## Клетки (Cages)

**GET**: `/api/v1/rows/{rowId}/cage`

Назначение: получение списка всех клеток в ряду.

Параметры:
- `rowId` (path) - идентификатор ряда

Ответ:
```json
{
  "message": "",
  "payload": [
    {
      "id": 1,
      "cageNumber": 1,
      "rowId": 1,
      "version": 0
    },
    {
      "id": 2,
      "cageNumber": 2,
      "rowId": 1,
      "version": 0
    }
  ],
  "success": true
}
```

**GET**: `/api/v1/rows/{rowId}/cage/{cageNumber}`

Назначение: получение клетки по номеру в ряду.

Параметры:
- `rowId` (path) - идентификатор ряда
- `cageNumber` (path) - номер клетки

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 1,
    "cageNumber": 1,
    "rowId": 1,
    "version": 0
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"0"`

**POST**: `/api/v1/rows/{rowId}/cage`

Назначение: создание новой клетки в ряду.

Параметры:
- `rowId` (path) - идентификатор ряда

Тело запроса:
```json
{
  "cageNumber": 3
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 3,
    "cageNumber": 3,
    "rowId": 1,
    "version": 0
  },
  "success": true
}
```

Заголовки ответа:
- `Location`: `/api/v1/rows/1/cage/3`
- `ETag`: `"0"`

**PUT**: `/api/v1/rows/{rowId}/cage/{cageNumber}`

Назначение: полная замена клетки по номеру в ряду.

Параметры:
- `rowId` (path) - идентификатор ряда
- `cageNumber` (path) - номер клетки

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Тело запроса:
```json
{
  "cageNumber": 4
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 1,
    "cageNumber": 4,
    "rowId": 1,
    "version": 1
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"1"`

**PATCH**: `/api/v1/rows/{rowId}/cage/{cageNumber}`

Назначение: частичное обновление клетки по номеру в ряду.

Параметры:
- `rowId` (path) - идентификатор ряда
- `cageNumber` (path) - номер клетки

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Тело запроса (все поля опциональны):
```json
{
  "cageNumber": 5
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 1,
    "cageNumber": 5,
    "rowId": 1,
    "version": 2
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"2"`

**DELETE**: `/api/v1/rows/{rowId}/cage/{cageNumber}`

Назначение: удаление клетки по номеру в ряду.

Параметры:
- `rowId` (path) - идентификатор ряда
- `cageNumber` (path) - номер клетки

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Ответ: 204 No Content

---

## Назначение клеток работникам (Worker Cages)

**GET**: `/api/v1/workers/{workerId}/cages`

Назначение: получение всех клеток, назначенных работнику.

Параметры:
- `workerId` (path) - идентификатор работника

Ответ:
```json
{
  "message": "",
  "payload": [
    {
      "id": 1,
      "cageNumber": 1,
      "rowId": 1,
      "version": 0
    },
    {
      "id": 2,
      "cageNumber": 2,
      "rowId": 1,
      "version": 0
    }
  ],
  "success": true
}
```

**GET**: `/api/v1/workers/cages/{cageId}/workers`

Назначение: получение всех работников, назначенных на клетку.

Параметры:
- `cageId` (path) - идентификатор клетки

Ответ:
```json
{
  "message": "",
  "payload": [
    {
      "id": 1,
      "firstName": "Ivan",
      "lastName": "Ivanov",
      "patronymic": "Petrovich",
      "cages": [],
      "version": 0
    }
  ],
  "success": true
}
```

**POST**: `/api/v1/workers/{workerId}/cages/{cageId}`

Назначение: назначение клетки работнику.

Параметры:
- `workerId` (path) - идентификатор работника
- `cageId` (path) - идентификатор клетки

Ответ: 201 Created
```json
{
  "message": "",
  "payload": null,
  "success": true
}
```

**DELETE**: `/api/v1/workers/{workerId}/cages/{cageId}`

Назначение: снятие назначения клетки с работника.

Параметры:
- `workerId` (path) - идентификатор работника
- `cageId` (path) - идентификатор клетки

Ответ: 204 No Content

---

## Породы (Breeds)

**POST**: `/api/v1/breeds`

Назначение: создание новой породы. Название должно быть уникальным.

Тело запроса:
```json
{
  "name": "Leghorn",
  "eggsNumber": 280,
  "weight": 2500
}
```

Ответ: 201 Created
```json
{
  "message": "",
  "payload": {
    "id": 3,
    "name": "Leghorn",
    "eggsNumber": 280,
    "weight": 2500,
    "version": 0
  },
  "success": true
}
```

Заголовки ответа:
- `Location`: `/api/v1/breeds/3`
- `ETag`: `"0"`

**GET**: `/api/v1/breeds`

Назначение: получение списка всех активных пород.

Ответ:
```json
{
  "message": "",
  "payload": [
    {
      "id": 3,
      "name": "Leghorn",
      "eggsNumber": 280,
      "weight": 2500,
      "version": 0
    },
    {
      "id": 4,
      "name": "Rhode Island Red",
      "eggsNumber": 260,
      "weight": 3000,
      "version": 0
    }
  ],
  "success": true
}
```

**GET**: `/api/v1/breeds/{id}`

Назначение: получение породы по идентификатору.

Параметры:
- `id` (path) - идентификатор породы

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 3,
    "name": "Leghorn",
    "eggsNumber": 280,
    "weight": 2500,
    "version": 0
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"0"`

**PUT**: `/api/v1/breeds/{id}`

Назначение: полная замена породы по идентификатору.

Параметры:
- `id` (path) - идентификатор породы

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Тело запроса:
```json
{
  "name": "Leghorn Modified",
  "eggsNumber": 300,
  "weight": 2700
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 3,
    "name": "Leghorn Modified",
    "eggsNumber": 300,
    "weight": 2700,
    "version": 1
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"1"`

**PATCH**: `/api/v1/breeds/{id}`

Назначение: частичное обновление породы по идентификатору.

Параметры:
- `id` (path) - идентификатор породы

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Тело запроса (все поля опциональны):
```json
{
  "name": "Leghorn Updated"
}
```

Или:
```json
{
  "eggsNumber": 290,
  "weight": 2600
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 3,
    "name": "Leghorn Updated",
    "eggsNumber": 290,
    "weight": 2600,
    "version": 2
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"2"`

**DELETE**: `/api/v1/breeds/{id}`

Назначение: удаление породы по идентификатору.

Параметры:
- `id` (path) - идентификатор породы

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Ответ: 204 No Content

---

## Куры (Chickens)

**POST**: `/api/v1/chickens`

Назначение: создание новой курицы.

Тело запроса:
```json
{
  "name": "Clucky",
  "weight": 2500,
  "birthDate": "2023-01-15",
  "breedId": 1,
  "cageId": 5
}
```

Ответ: 201 Created
```json
{
  "message": "",
  "payload": {
    "id": 10,
    "name": "Clucky",
    "weight": 2500,
    "birthDate": "2023-01-15",
    "breedId": 1,
    "cageId": 5,
    "version": 0
  },
  "success": true
}
```

Заголовки ответа:
- `Location`: `/api/v1/chickens/10`
- `ETag`: `"0"`

**GET**: `/api/v1/chickens`

Назначение: получение списка всех кур.

Ответ:
```json
{
  "message": "",
  "payload": [
    {
      "id": 10,
      "name": "Clucky",
      "weight": 2500,
      "birthDate": "2023-01-15",
      "breedId": 1,
      "cageId": 5,
      "version": 0
    },
    {
      "id": 11,
      "name": "Feathers",
      "weight": 2300,
      "birthDate": "2023-03-20",
      "breedId": 2,
      "cageId": 5,
      "version": 0
    }
  ],
  "success": true
}
```

**GET**: `/api/v1/chickens/{id}`

Назначение: получение курицы по идентификатору.

Параметры:
- `id` (path) - идентификатор курицы

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 10,
    "name": "Clucky",
    "weight": 2500,
    "birthDate": "2023-01-15",
    "breedId": 1,
    "cageId": 5,
    "version": 0
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"0"`

**PUT**: `/api/v1/chickens/{id}`

Назначение: полная замена курицы по идентификатору.

Параметры:
- `id` (path) - идентификатор курицы

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Тело запроса:
```json
{
  "name": "Clucky Updated",
  "weight": 2600,
  "birthDate": "2023-01-15",
  "breedId": 1,
  "cageId": 6
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 10,
    "name": "Clucky Updated",
    "weight": 2600,
    "birthDate": "2023-01-15",
    "breedId": 1,
    "cageId": 6,
    "version": 1
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"1"`

**PATCH**: `/api/v1/chickens/{id}`

Назначение: частичное обновление курицы по идентификатору.

Параметры:
- `id` (path) - идентификатор курицы

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Тело запроса (все поля опциональны):
```json
{
  "weight": 2700
}
```

Или:
```json
{
  "name": "Clucky New",
  "cageId": 7
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 10,
    "name": "Clucky New",
    "weight": 2700,
    "birthDate": "2023-01-15",
    "breedId": 1,
    "cageId": 7,
    "version": 2
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"2"`

**DELETE**: `/api/v1/chickens/{id}`

Назначение: удаление курицы по идентификатору.

Параметры:
- `id` (path) - идентификатор курицы

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Ответ: 204 No Content

---

## Перемещения кур (Chicken Movements)

**GET**: `/api/v1/chicken-movements/{id}`

Назначение: получение перемещения по идентификатору.

Параметры:
- `id` (path) - идентификатор перемещения

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 15,
    "chickenId": 7,
    "fromCageId": 5,
    "toCageId": 8,
    "movedAt": "2024-01-15T10:30:00"
  },
  "success": true
}
```

**GET**: `/api/v1/chickens/{chickenId}/movements`

Назначение: получение всех перемещений курицы, отсортированных от новых к старым.

Параметры:
- `chickenId` (path) - идентификатор курицы

Ответ:
```json
{
  "message": "",
  "payload": [
    {
      "id": 15,
      "chickenId": 7,
      "fromCageId": 8,
      "toCageId": 10,
      "movedAt": "2024-01-20T14:00:00"
    },
    {
      "id": 14,
      "chickenId": 7,
      "fromCageId": 5,
      "toCageId": 8,
      "movedAt": "2024-01-15T10:30:00"
    }
  ],
  "success": true
}
```

**GET**: `/api/v1/chickens/{chickenId}/movements/current`

Назначение: получение текущего местоположения курицы (последнее перемещение, текущая клетка определяется по `toCageId`).

Параметры:
- `chickenId` (path) - идентификатор курицы

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 15,
    "chickenId": 7,
    "fromCageId": 8,
    "toCageId": 10,
    "movedAt": "2024-01-20T14:00:00"
  },
  "success": true
}
```

**POST**: `/api/v1/chickens/{chickenId}/movements`

Назначение: создание нового перемещения (переселения) курицы. Если `fromCageId` не указан, используется текущая клетка курицы (может быть null для первого размещения). `toCageId` обязателен.

Параметры:
- `chickenId` (path) - идентификатор курицы

Тело запроса:
```json
{
  "fromCageId": 5,
  "toCageId": 8
}
```

Или (без fromCageId):
```json
{
  "toCageId": 8
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 16,
    "chickenId": 7,
    "fromCageId": 5,
    "toCageId": 8,
    "movedAt": "2024-01-21T09:00:00"
  },
  "success": true
}
```

---

## Производство яиц по месяцам (Egg Production Month)

**GET**: `/api/v1/chickens/{chickenId}/egg-productions`

Назначение: получение всех записей производства яиц для курицы.

Параметры:
- `chickenId` (path) - идентификатор курицы

Ответ:
```json
{
  "message": "",
  "payload": [
    {
      "id": 1,
      "month": 1,
      "year": 2024,
      "count": 25,
      "chickenId": 1,
      "version": 0
    },
    {
      "id": 2,
      "month": 2,
      "year": 2024,
      "count": 28,
      "chickenId": 1,
      "version": 0
    }
  ],
  "success": true
}
```

**GET**: `/api/v1/chickens/{chickenId}/egg-productions/{year}`

Назначение: получение всех записей производства яиц для курицы за год.

Параметры:
- `chickenId` (path) - идентификатор курицы
- `year` (path) - год

Ответ:
```json
{
  "message": "",
  "payload": [
    {
      "id": 1,
      "month": 1,
      "year": 2024,
      "count": 25,
      "chickenId": 1,
      "version": 0
    },
    {
      "id": 2,
      "month": 2,
      "year": 2024,
      "count": 28,
      "chickenId": 1,
      "version": 0
    }
  ],
  "success": true
}
```

**GET**: `/api/v1/chickens/{chickenId}/egg-productions/{year}/{month}`

Назначение: получение записи производства яиц для курицы за конкретный месяц и год.

Параметры:
- `chickenId` (path) - идентификатор курицы
- `year` (path) - год
- `month` (path) - месяц (1-12)

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 1,
    "month": 1,
    "year": 2024,
    "count": 25,
    "chickenId": 1,
    "version": 0
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"0"`

**POST**: `/api/v1/chickens/{chickenId}/egg-productions/{year}/{month}`

Назначение: создание записи производства яиц для курицы за месяц и год.

Параметры:
- `chickenId` (path) - идентификатор курицы
- `year` (path) - год
- `month` (path) - месяц (1-12)

Тело запроса:
```json
{
  "count": 25
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 1,
    "month": 1,
    "year": 2024,
    "count": 25,
    "chickenId": 1,
    "version": 0
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"0"`

**PUT**: `/api/v1/chickens/{chickenId}/egg-productions/{year}/{month}`

Назначение: полная замена записи производства яиц для курицы за месяц и год.

Параметры:
- `chickenId` (path) - идентификатор курицы
- `year` (path) - год
- `month` (path) - месяц (1-12)

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Тело запроса:
```json
{
  "count": 30
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 1,
    "month": 1,
    "year": 2024,
    "count": 30,
    "chickenId": 1,
    "version": 1
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"1"`

**PATCH**: `/api/v1/chickens/{chickenId}/egg-productions/{year}/{month}`

Назначение: частичное обновление записи производства яиц для курицы за месяц и год.

Параметры:
- `chickenId` (path) - идентификатор курицы
- `year` (path) - год
- `month` (path) - месяц (1-12)

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Тело запроса (все поля опциональны):
```json
{
  "count": 32
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 1,
    "month": 1,
    "year": 2024,
    "count": 32,
    "chickenId": 1,
    "version": 2
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"2"`

**DELETE**: `/api/v1/chickens/{chickenId}/egg-productions/{year}/{month}`

Назначение: удаление записи производства яиц для курицы за месяц и год.

Параметры:
- `chickenId` (path) - идентификатор курицы
- `year` (path) - год
- `month` (path) - месяц (1-12)

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Ответ: 204 No Content

---

## Рационы (Diets)

**GET**: `/api/v1/diets`

Назначение: получение списка всех рационов в системе.

Ответ:
```json
{
  "message": "",
  "payload": [
    {
      "id": 1,
      "title": "Летний рацион",
      "code": "SUMMER-001",
      "description": "Рацион для летнего периода",
      "season": "SUMMER",
      "version": 0
    },
    {
      "id": 2,
      "title": "Зимний рацион",
      "code": "WINTER-001",
      "description": "Рацион для зимнего периода",
      "season": "WINTER",
      "version": 0
    }
  ],
  "success": true
}
```

**GET**: `/api/v1/diets/{id}`

Назначение: получение рациона по идентификатору.

Параметры:
- `id` (path) - идентификатор рациона

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 1,
    "title": "Летний рацион",
    "code": "SUMMER-001",
    "description": "Рацион для летнего периода",
    "season": "SUMMER",
    "version": 0
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"0"`

**POST**: `/api/v1/diets`

Назначение: создание нового рациона.

Тело запроса:
```json
{
  "title": "Летний рацион",
  "code": "SUMMER-001",
  "description": "Рацион для летнего периода",
  "season": "SUMMER"
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 1,
    "title": "Летний рацион",
    "code": "SUMMER-001",
    "description": "Рацион для летнего периода",
    "season": "SUMMER",
    "version": 0
  },
  "success": true
}
```

Заголовки ответа:
- `Location`: `/api/v1/diets/1`
- `ETag`: `"0"`

**PUT**: `/api/v1/diets/{id}`

Назначение: полная замена рациона по идентификатору.

Параметры:
- `id` (path) - идентификатор рациона

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Тело запроса:
```json
{
  "title": "Летний рацион обновленный",
  "code": "SUMMER-002",
  "description": "Обновленный рацион для летнего периода",
  "season": "SUMMER"
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 1,
    "title": "Летний рацион обновленный",
    "code": "SUMMER-002",
    "description": "Обновленный рацион для летнего периода",
    "season": "SUMMER",
    "version": 1
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"1"`

**PATCH**: `/api/v1/diets/{id}`

Назначение: частичное обновление рациона по идентификатору.

Параметры:
- `id` (path) - идентификатор рациона

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Тело запроса (все поля опциональны):
```json
{
  "title": "Летний рацион улучшенный"
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 1,
    "title": "Летний рацион улучшенный",
    "code": "SUMMER-002",
    "description": "Обновленный рацион для летнего периода",
    "season": "SUMMER",
    "version": 2
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"2"`

**DELETE**: `/api/v1/diets/{id}`

Назначение: удаление рациона по идентификатору.

Параметры:
- `id` (path) - идентификатор рациона

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Ответ: 204 No Content

---

## Увольнения (Dismissals)

**GET**: `/api/v1/dismissals/workers/{workerId}`

Назначение: получение всех увольнений работника.

Параметры:
- `workerId` (path) - идентификатор работника

Ответ:
```json
{
  "message": "",
  "payload": [
    {
      "id": 1,
      "dismissalDate": "2024-01-15",
      "reason": "По собственному желанию",
      "worker": "Ivan Ivanov",
      "whoDismiss": "Petr Petrov",
      "version": 0
    }
  ],
  "success": true
}
```

**GET**: `/api/v1/dismissals/dismissed/{dismissedId}`

Назначение: получение всех увольнений, выполненных конкретным пользователем.

Параметры:
- `dismissedId` (path) - идентификатор пользователя, который выполнил увольнение

Ответ:
```json
{
  "message": "",
  "payload": [
    {
      "id": 1,
      "dismissalDate": "2024-01-15",
      "reason": "По собственному желанию",
      "worker": "Ivan Ivanov",
      "whoDismiss": "Petr Petrov",
      "version": 0
    }
  ],
  "success": true
}
```

**GET**: `/api/v1/dismissals/workers/{workerId}/dismissed/{dismissedId}`

Назначение: получение увольнения по работнику и пользователю, который выполнил увольнение.

Параметры:
- `workerId` (path) - идентификатор работника
- `dismissedId` (path) - идентификатор пользователя, который выполнил увольнение

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 1,
    "dismissalDate": "2024-01-15",
    "reason": "По собственному желанию",
    "worker": "Ivan Ivanov",
    "whoDismiss": "Petr Petrov",
    "version": 0
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"0"`

**POST**: `/api/v1/dismissals`

Назначение: создание нового увольнения.

Тело запроса:
```json
{
  "workerId": 1,
  "dismissalDate": "2024-01-15",
  "reason": "По собственному желанию"
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 1,
    "dismissalDate": "2024-01-15",
    "reason": "По собственному желанию",
    "worker": "Ivan Ivanov",
    "whoDismiss": "Current User",
    "version": 0
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"0"`

**PUT**: `/api/v1/dismissals/{workerId}`

Назначение: полная замена увольнения по идентификатору работника.

Параметры:
- `workerId` (path) - идентификатор работника

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Тело запроса:
```json
{
  "dismissalDate": "2024-01-16",
  "reason": "По соглашению сторон"
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 1,
    "dismissalDate": "2024-01-16",
    "reason": "По соглашению сторон",
    "worker": "Ivan Ivanov",
    "whoDismiss": "Petr Petrov",
    "version": 1
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"1"`

**PATCH**: `/api/v1/dismissals/{workerId}`

Назначение: частичное обновление увольнения по идентификатору работника.

Параметры:
- `workerId` (path) - идентификатор работника

Заголовки запроса:
- `If-Match` (обязательный) - ETag текущей версии ресурса

Тело запроса (все поля опциональны):
```json
{
  "reason": "Обновленная причина"
}
```

Ответ:
```json
{
  "message": "",
  "payload": {
    "id": 1,
    "dismissalDate": "2024-01-16",
    "reason": "Обновленная причина",
    "worker": "Ivan Ivanov",
    "whoDismiss": "Petr Petrov",
    "version": 2
  },
  "success": true
}
```

Заголовки ответа:
- `ETag`: `"2"`

---

## Отчеты директора (Director Reports)

**GET**: `/api/v1/reports/director/factory/monthly?year={year}&month={month}`

Назначение: получение месячного отчета по всей фабрике с агрегированными метриками.

Параметры:
- `year` (query, обязательный) - год
- `month` (query, обязательный) - месяц (1-12)

Ответ:
```json
{
  "message": "",
  "payload": {
    "totalEggs": 15000,
    "totalChickens": 500,
    "averageEggsPerChicken": 30
  },
  "success": true
}
```

**GET**: `/api/v1/reports/director/breeds/egg-diff`

Назначение: получение отчета о разнице между метриками каждой породы и средними показателями фабрики.

Ответ:
```json
{
  "message": "",
  "payload": [
    {
      "breedId": 1,
      "breedName": "Leghorn",
      "eggsDifference": 5.2,
      "factoryAverage": 30
    }
  ],
  "success": true
}
```

**GET**: `/api/v1/reports/director/chickens/by-workshop-and-breed`

Назначение: получение распределения кур по цехам и породам (сколько кур каждой породы находится в каждом цехе).

Ответ:
```json
{
  "message": "",
  "payload": [
    {
      "workshopId": 1,
      "workshopNumber": 1,
      "breedId": 1,
      "breedName": "Leghorn",
      "chickenCount": 150
    }
  ],
  "success": true
}
```

**GET**: `/api/v1/reports/director/chickens/top-workshop-by-breed?breedId={breedId}`

Назначение: получение цеха с наибольшим количеством кур указанной породы.

Параметры:
- `breedId` (query, обязательный) - идентификатор породы

Ответ:
```json
{
  "message": "",
  "payload": {
    "workshopId": 1,
    "workshopNumber": 1,
    "breedId": 1,
    "breedName": "Leghorn",
    "chickenCount": 150
  },
  "success": true
}
```

**GET**: `/api/v1/reports/director/chickens/egg-stats?weight={weight}&breedId={breedId}&birthDate={birthDate}`

Назначение: получение статистики по яйцам для каждой курицы с фильтрацией по весу, породе или дате рождения.

Параметры:
- `weight` (query, опциональный) - фильтр по весу курицы
- `breedId` (query, опциональный) - фильтр по идентификатору породы
- `birthDate` (query, опциональный) - фильтр по дате рождения (формат: YYYY-MM-DD)

Ответ:
```json
{
  "message": "",
  "payload": [
    {
      "chickenId": 1,
      "chickenName": "Clucky",
      "totalEggs": 300,
      "averageEggsPerMonth": 25
    }
  ],
  "success": true
}
```

**GET**: `/api/v1/reports/director/workers/daily-avg-eggs?year={year}&month={month}`

Назначение: получение среднего количества яиц в день, собранных каждым работником за указанный месяц.

Параметры:
- `year` (query, обязательный) - год
- `month` (query, обязательный) - месяц (1-12)

Ответ:
```json
{
  "message": "",
  "payload": [
    {
      "workerId": 1,
      "workerName": "Ivan Ivanov",
      "dailyAverageEggs": 150.5
    }
  ],
  "success": true
}
```
