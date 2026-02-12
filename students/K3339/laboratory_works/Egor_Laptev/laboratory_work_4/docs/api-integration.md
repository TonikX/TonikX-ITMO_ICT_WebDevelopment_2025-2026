# API взаимодействие

Документация описывает механизм взаимодействия Vue 3 приложения с Django REST Framework API.

## Архитектура взаимодействия

Frontend приложение взаимодействует с Backend API через HTTP запросы, используя библиотеку Axios. Все API вызовы централизованы в сервисе `api.js`.

## Расположение

Сервис API находится в файле `src/services/api.js`

## Конфигурация Axios

### Базовый URL

```javascript
const API_BASE_URL = 'http://localhost:8000'
```

API сервер должен быть запущен на порту 8000. Для production окружения необходимо изменить этот URL.

### Создание экземпляра Axios

```javascript
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})
```

## Interceptors

### Request Interceptor

Автоматически добавляет токен авторизации к каждому запросу:

```javascript
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Token ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)
```

### Response Interceptor

Обрабатывает ошибки авторизации и автоматически перенаправляет на страницу входа:

```javascript
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)
```

## API методы

Все методы для работы с API сгруппированы в двух объектах: `authAPI` (аутентификация) и `hotelAPI` (управление отелем).

### Авторизация

#### login(username, password)

Выполняет вход пользователя в систему.

**Endpoint:** `POST /auth/token/login/`

**Параметры:**
- `username` (string) - имя пользователя
- `password` (string) - пароль

**Возвращает:** Promise с объектом ответа, содержащим `auth_token`

**Пример:**
```javascript
const response = await authAPI.login('username', 'password')
localStorage.setItem('auth_token', response.data.auth_token)
```

#### logout()

Выполняет выход пользователя из системы.

**Endpoint:** `POST /auth/token/logout/`

**Требует:** Токен авторизации в заголовке

**Возвращает:** Promise

**Пример:**
```javascript
await authAPI.logout()
localStorage.removeItem('auth_token')
```

### Регистрация

#### register(username, password, email)

Регистрирует нового пользователя в системе.

**Endpoint:** `POST /auth/users/`

**Параметры:**
- `username` (string) - имя пользователя
- `password` (string) - пароль
- `email` (string) - email адрес

**Возвращает:** Promise с данными созданного пользователя

**Пример:**
```javascript
const response = await authAPI.register('newuser', 'password123', 'user@example.com')
```

### Управление профилем

#### getCurrentUser()

Получает данные текущего авторизованного пользователя.

**Endpoint:** `GET /auth/users/me/`

**Требует:** Токен авторизации в заголовке

**Возвращает:** Promise с данными пользователя

**Пример:**
```javascript
const response = await authAPI.getCurrentUser()
console.log(response.data.username, response.data.email)
```

#### updateUser(data)

Обновляет данные текущего пользователя.

**Endpoint:** `PATCH /auth/users/me/`

**Требует:** Токен авторизации в заголовке

**Параметры:**
- `data` (object) - объект с полями для обновления:
  - `username` (string, опционально)
  - `email` (string, опционально)

**Возвращает:** Promise с обновленными данными пользователя

**Пример:**
```javascript
await authAPI.updateUser({
  username: 'newusername',
  email: 'newemail@example.com'
})
```

#### changePassword(currentPassword, newPassword)

Изменяет пароль текущего пользователя.

**Endpoint:** `POST /auth/users/set_password/`

**Требует:** Токен авторизации в заголовке

**Параметры:**
- `currentPassword` (string) - текущий пароль
- `newPassword` (string) - новый пароль

**Возвращает:** Promise

**Пример:**
```javascript
await authAPI.changePassword('oldpassword', 'newpassword123')
```

## Hotel API методы

Все методы для работы с данными отеля сгруппированы в объекте `hotelAPI`:

### Типы номеров

#### roomTypes.list()

Получает список всех типов номеров.

**Endpoint:** `GET /api/room-types/`

**Возвращает:** Promise с массивом типов номеров

**Пример:**
```javascript
const response = await hotelAPI.roomTypes.list()
console.log(response.data)
```

#### roomTypes.get(id)

Получает конкретный тип номера по ID.

**Endpoint:** `GET /api/room-types/{id}/`

**Параметры:**
- `id` (number) - ID типа номера

**Возвращает:** Promise с данными типа номера

#### roomTypes.create(data)

Создает новый тип номера.

**Endpoint:** `POST /api/room-types/`

**Параметры:**
- `data` (object) - объект с полями:
  - `name` (string) - название типа
  - `capacity` (number) - вместимость
  - `price_per_day` (number) - цена за день

**Возвращает:** Promise с данными созданного типа номера

#### roomTypes.update(id, data)

Обновляет тип номера.

**Endpoint:** `PUT /api/room-types/{id}/`

**Параметры:**
- `id` (number) - ID типа номера
- `data` (object) - объект с полями для обновления

#### roomTypes.patch(id, data)

Частично обновляет тип номера.

**Endpoint:** `PATCH /api/room-types/{id}/`

#### roomTypes.delete(id)

Удаляет тип номера.

**Endpoint:** `DELETE /api/room-types/{id}/`

#### roomTypes.stats()

Получает статистику по типам номеров.

**Endpoint:** `GET /api/room-types/stats/`

**Возвращает:** Promise с массивом статистики (включая количество номеров каждого типа)

### Этажи

#### floors.list()

Получает список всех этажей.

**Endpoint:** `GET /api/floors/`

#### floors.get(id)

Получает конкретный этаж по ID.

**Endpoint:** `GET /api/floors/{id}/`

#### floors.create(data)

Создает новый этаж.

**Endpoint:** `POST /api/floors/`

**Параметры:**
- `data` (object) - объект с полем `number` (number)

#### floors.update(id, data)

Обновляет этаж.

**Endpoint:** `PUT /api/floors/{id}/`

#### floors.patch(id, data)

Частично обновляет этаж.

**Endpoint:** `PATCH /api/floors/{id}/`

#### floors.delete(id)

Удаляет этаж.

**Endpoint:** `DELETE /api/floors/{id}/`

#### floors.stats()

Получает статистику по этажам.

**Endpoint:** `GET /api/floors/stats/`

**Возвращает:** Promise с массивом статистики (включая количество номеров и уборок на каждом этаже)

### Номера

#### rooms.list()

Получает список всех номеров.

**Endpoint:** `GET /api/rooms/`

#### rooms.get(id)

Получает конкретный номер по ID.

**Endpoint:** `GET /api/rooms/{id}/`

#### rooms.create(data)

Создает новый номер.

**Endpoint:** `POST /api/rooms/`

**Параметры:**
- `data` (object) - объект с полями:
  - `number` (string) - номер комнаты
  - `phone` (string, опционально) - телефон
  - `type_id` (number) - ID типа номера
  - `floor_id` (number) - ID этажа

#### rooms.update(id, data)

Обновляет номер.

**Endpoint:** `PUT /api/rooms/{id}/`

#### rooms.patch(id, data)

Частично обновляет номер.

**Endpoint:** `PATCH /api/rooms/{id}/`

#### rooms.delete(id)

Удаляет номер.

**Endpoint:** `DELETE /api/rooms/{id}/`

### Гости

#### guests.list()

Получает список всех гостей.

**Endpoint:** `GET /api/guests/`

#### guests.get(id)

Получает конкретного гостя по ID.

**Endpoint:** `GET /api/guests/{id}/`

#### guests.create(data)

Создает нового гостя.

**Endpoint:** `POST /api/guests/`

**Параметры:**
- `data` (object) - объект с полями:
  - `passport_number` (string) - номер паспорта
  - `last_name` (string) - фамилия
  - `first_name` (string) - имя
  - `middle_name` (string, опционально) - отчество
  - `city` (string) - город

#### guests.update(id, data)

Обновляет гостя.

**Endpoint:** `PUT /api/guests/{id}/`

#### guests.patch(id, data)

Частично обновляет гостя.

**Endpoint:** `PATCH /api/guests/{id}/`

#### guests.delete(id)

Удаляет гостя.

**Endpoint:** `DELETE /api/guests/{id}/`

### Проживания

#### stays.list()

Получает список всех проживаний.

**Endpoint:** `GET /api/stays/`

#### stays.get(id)

Получает конкретное проживание по ID.

**Endpoint:** `GET /api/stays/{id}/`

#### stays.create(data)

Создает новое проживание.

**Endpoint:** `POST /api/stays/`

**Параметры:**
- `data` (object) - объект с полями:
  - `guest_id` (number) - ID гостя
  - `room_id` (number) - ID номера
  - `check_in` (string) - дата заезда (YYYY-MM-DD)
  - `check_out` (string) - дата выезда (YYYY-MM-DD)

#### stays.update(id, data)

Обновляет проживание.

**Endpoint:** `PUT /api/stays/{id}/`

#### stays.patch(id, data)

Частично обновляет проживание.

**Endpoint:** `PATCH /api/stays/{id}/`

#### stays.delete(id)

Удаляет проживание.

**Endpoint:** `DELETE /api/stays/{id}/`

#### stays.summary(date)

Получает сводку по проживаниям на определенную дату.

**Endpoint:** `GET /api/stays/summary/?date=YYYY-MM-DD`

**Параметры:**
- `date` (string, опционально) - дата в формате YYYY-MM-DD (по умолчанию - сегодня)

**Возвращает:** Promise с объектом сводки:
```json
{
  "date": "2024-01-18",
  "total_stays": 50,
  "active_now": 12,
  "upcoming": 8,
  "active_rooms": 10
}
```

### Сотрудники

#### employees.list()

Получает список всех сотрудников.

**Endpoint:** `GET /api/employees/`

#### employees.get(id)

Получает конкретного сотрудника по ID.

**Endpoint:** `GET /api/employees/{id}/`

#### employees.create(data)

Создает нового сотрудника.

**Endpoint:** `POST /api/employees/`

**Параметры:**
- `data` (object) - объект с полями:
  - `last_name` (string) - фамилия
  - `first_name` (string) - имя
  - `middle_name` (string, опционально) - отчество
  - `employed` (boolean) - работает ли сотрудник

#### employees.update(id, data)

Обновляет сотрудника.

**Endpoint:** `PUT /api/employees/{id}/`

#### employees.patch(id, data)

Частично обновляет сотрудника.

**Endpoint:** `PATCH /api/employees/{id}/`

#### employees.delete(id)

Удаляет сотрудника.

**Endpoint:** `DELETE /api/employees/{id}/`

### График уборки

#### cleaning.list()

Получает список всех записей графика уборки.

**Endpoint:** `GET /api/cleaning/`

#### cleaning.get(id)

Получает конкретную запись по ID.

**Endpoint:** `GET /api/cleaning/{id}/`

#### cleaning.create(data)

Создает новую запись в графике уборки.

**Endpoint:** `POST /api/cleaning/`

**Параметры:**
- `data` (object) - объект с полями:
  - `weekday` (string) - день недели (monday, tuesday, wednesday, thursday, friday, saturday, sunday)
  - `employee_id` (number) - ID сотрудника
  - `floor_id` (number) - ID этажа

#### cleaning.update(id, data)

Обновляет запись в графике уборки.

**Endpoint:** `PUT /api/cleaning/{id}/`

#### cleaning.patch(id, data)

Частично обновляет запись в графике уборки.

**Endpoint:** `PATCH /api/cleaning/{id}/`

#### cleaning.delete(id)

Удаляет запись из графика уборки.

**Endpoint:** `DELETE /api/cleaning/{id}/`

## Обработка ошибок

### Типы ошибок

1. **400 Bad Request** - Ошибки валидации данных
   ```javascript
   {
     "username": ["Пользователь с таким именем уже существует."],
     "email": ["Пользователь с таким email уже существует."]
   }
   ```

2. **401 Unauthorized** - Ошибки авторизации
   - Отсутствует токен
   - Неверный токен
   - Токен истек

3. **404 Not Found** - Ресурс не найден

4. **500 Internal Server Error** - Ошибка сервера

### Пример обработки ошибок

```javascript
try {
  const response = await authAPI.login(username, password)
  // Обработка успешного ответа
} catch (error) {
  if (error.response) {
    // Сервер ответил с кодом ошибки
    const status = error.response.status
    const data = error.response.data
    
    if (status === 400) {
      // Обработка ошибок валидации
      console.error('Ошибка валидации:', data)
    } else if (status === 401) {
      // Обработка ошибок авторизации
      console.error('Ошибка авторизации:', data)
    }
  } else if (error.request) {
    // Запрос был отправлен, но ответа не получено
    console.error('Сервер не отвечает')
  } else {
    // Ошибка при настройке запроса
    console.error('Ошибка:', error.message)
  }
}
```

## Хранение токена

Токен авторизации хранится в `localStorage` браузера под ключом `auth_token`:

```javascript
// Сохранение токена
localStorage.setItem('auth_token', token)

// Получение токена
const token = localStorage.getItem('auth_token')

// Удаление токена
localStorage.removeItem('auth_token')
```

## CORS настройки

Для работы с API необходимо, чтобы на Django сервере были настроены CORS заголовки. В настройках Django (`settings.py`) должен быть установлен `corsheaders`:

```python
INSTALLED_APPS = [
    # ...
    'corsheaders',
]

MIDDLEWARE = [
    # ...
    'corsheaders.middleware.CorsMiddleware',
    # ...
]

CORS_ORIGIN_ALLOW_ALL = True  # Для разработки
# Или для production:
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:5173",
# ]
```

## Безопасность

### Рекомендации

1. **HTTPS в production**: Всегда используйте HTTPS для передачи токенов в production окружении

2. **Хранение токена**: Токен хранится в `localStorage`, что делает его доступным для XSS атак. Для повышения безопасности можно использовать httpOnly cookies

3. **Валидация на клиенте и сервере**: Валидация данных происходит как на клиенте (для UX), так и на сервере (для безопасности)

4. **Таймаут токена**: Реализовать механизм обновления токена при истечении срока действия

5. **Обработка ошибок**: Никогда не показывать пользователю детальные технические ошибки в production

## Тестирование API

Для тестирования API можно использовать инструменты:

- **Postman** - для отправки запросов и проверки endpoints
- **Swagger/ReDoc** - документация API на `/swagger/` или `/redoc/`
- **Browser DevTools** - Network tab для просмотра запросов и ответов



