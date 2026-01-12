# API: Аутентификация

Endpoints для регистрации, авторизации и управления профилем пользователя.

## Регистрация

### `POST /auth/register`

Регистрация нового пользователя в системе.

**Тело запроса:**

```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Параметры:**

| Поле | Тип | Обязательно | Описание |
|------|-----|-------------|----------|
| username | string | ✅ | Имя пользователя (3-150 символов) |
| email | string | ✅ | Email адрес |
| password | string | ✅ | Пароль (минимум 6 символов) |

**Успешный ответ (201 Created):**

```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2025-01-06T10:30:00"
}
```

**Ошибки:**

- `400 Bad Request` - пользователь с таким username/email уже существует
- `422 Unprocessable Entity` - невалидные данные

---

## Авторизация

### `POST /auth/login`

Авторизация пользователя и получение JWT токена.

**Тело запроса (form-data):**

```
username=john_doe
password=securepassword123
```

**Успешный ответ (200 OK):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huX2RvZSIsImV4cCI6MTYxNjI0NTIwMH0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
  "token_type": "bearer"
}
```

**Использование токена:**

Добавьте токен в заголовок всех защищённых запросов:

```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Ошибки:**

- `401 Unauthorized` - неверное имя пользователя или пароль

**Пример (curl):**

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john_doe&password=securepassword123"
```

**Пример (Python):**

```python
import requests

response = requests.post(
    "http://localhost:8000/auth/login",
    data={
        "username": "john_doe",
        "password": "securepassword123"
    }
)

token = response.json()["access_token"]
```

---

## Информация о текущем пользователе

### `GET /auth/me`

Получение информации о текущем авторизованном пользователе.

**Требуется авторизация:** ✅

**Успешный ответ (200 OK):**

```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2025-01-06T10:30:00"
}
```

**Ошибки:**

- `401 Unauthorized` - токен отсутствует или невалиден

**Пример (curl):**

```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Получение профиля

### `GET /auth/me/profile`

Получение профиля текущего пользователя.

**Требуется авторизация:** ✅

**Успешный ответ (200 OK):**

```json
{
  "id": 1,
  "user_id": 1,
  "date_of_birth": "1990-05-15"
}
```

**Ошибки:**

- `401 Unauthorized` - токен отсутствует или невалиден
- `404 Not Found` - профиль не найден

---

## Обновление профиля

### `PUT /auth/me/profile`

Обновление профиля текущего пользователя.

**Требуется авторизация:** ✅

**Тело запроса:**

```json
{
  "date_of_birth": "1990-05-15"
}
```

**Параметры:**

| Поле | Тип | Обязательно | Описание |
|------|-----|-------------|----------|
| date_of_birth | string (date) | ❌ | Дата рождения (формат: YYYY-MM-DD) |

**Успешный ответ (200 OK):**

```json
{
  "id": 1,
  "user_id": 1,
  "date_of_birth": "1990-05-15"
}
```

**Ошибки:**

- `401 Unauthorized` - токен отсутствует или невалиден
- `404 Not Found` - профиль не найден
- `422 Unprocessable Entity` - невалидная дата

**Пример (curl):**

```bash
curl -X PUT "http://localhost:8000/auth/me/profile" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"date_of_birth": "1990-05-15"}'
```

---

## Полный пример использования

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. Регистрация
register_response = requests.post(
    f"{BASE_URL}/auth/register",
    json={
        "username": "john_doe",
        "email": "john@example.com",
        "password": "securepassword123"
    }
)
print("Пользователь создан:", register_response.json())

# 2. Авторизация
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    data={
        "username": "john_doe",
        "password": "securepassword123"
    }
)
token = login_response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# 3. Получение информации о пользователе
me_response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
print("Информация о пользователе:", me_response.json())

# 4. Обновление профиля
profile_response = requests.put(
    f"{BASE_URL}/auth/me/profile",
    headers=headers,
    json={"date_of_birth": "1990-05-15"}
)
print("Профиль обновлён:", profile_response.json())
```

---

## Время жизни токена

JWT токены имеют ограниченное время жизни (по умолчанию 30 минут).

После истечения срока действия токена необходимо:
1. Выполнить повторную авторизацию
2. Получить новый токен
3. Использовать новый токен в запросах

!!! warning "Безопасность"
    - Храните токены в безопасном месте
    - Не передавайте токены по незащищённым каналам
    - Не храните токены в открытом виде в коде
