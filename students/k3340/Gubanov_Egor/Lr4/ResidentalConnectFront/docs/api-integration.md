# API Интеграция

## Обзор

Приложение взаимодействует с Django REST Framework бэкендом через HTTP API. Для работы с API используется библиотека **Axios** с настроенными interceptors для автоматической обработки токенов и ошибок.

## Базовый URL

По умолчанию API доступен по адресу `http://127.0.0.1:8000`.

Для изменения создайте файл `.env`:
```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## Настройка Axios

Файл: `src/services/api.js`

### Базовый клиент

```javascript
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})
```

### Interceptors

#### Request Interceptor

Автоматически добавляет токен авторизации к каждому запросу:

```javascript
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    config.headers.Authorization = `Token ${token}`
  }
  return config
})
```

#### Response Interceptor

Обрабатывает ошибки авторизации:

```javascript
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Токен недействителен
      localStorage.removeItem('auth_token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)
```

## Сервисы

### Auth Service

Файл: `src/services/authService.js`

Методы для работы с аутентификацией:

#### Регистрация

```javascript
async register(userData) {
  const response = await api.post('/api/auth/users/', userData)
  return response.data
}
```

**Endpoint:** `POST /api/auth/users/`

**Параметры:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "first_name": "string",
  "last_name": "string",
  "role": "resident|master|dispatcher",
  "phone_number": "string",
  "address": "string"
}
```

#### Вход

```javascript
async login(username, password) {
  const response = await api.post('/api/auth/token/login/', {
    username,
    password,
  })
  return response.data
}
```

**Endpoint:** `POST /api/auth/token/login/`

**Параметры:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Ответ:**
```json
{
  "auth_token": "string"
}
```

#### Выход

```javascript
async logout() {
  await api.post('/api/auth/token/logout/')
}
```

**Endpoint:** `POST /api/auth/token/logout/`

**Требования:** Токен в заголовке `Authorization`

#### Получение текущего пользователя

```javascript
async getCurrentUser() {
  const response = await api.get('/api/auth/users/me/')
  return response.data
}
```

**Endpoint:** `GET /api/auth/users/me/`

**Требования:** Токен в заголовке `Authorization`

#### Обновление профиля

```javascript
async updateUser(userData) {
  const response = await api.patch('/api/auth/users/me/', userData)
  return response.data
}
```

**Endpoint:** `PATCH /api/auth/users/me/`

**Требования:** Токен в заголовке `Authorization`

**Параметры:** Любые поля пользователя (кроме `username` и `role`)

#### Смена пароля

```javascript
async changePassword(currentPassword, newPassword) {
  const response = await api.post('/api/auth/users/set_password/', {
    current_password: currentPassword,
    new_password: newPassword,
  })
  return response.data
}
```

**Endpoint:** `POST /api/auth/users/set_password/`

**Требования:** Токен в заголовке `Authorization`

**Параметры:**
```json
{
  "current_password": "string",
  "new_password": "string"
}
```

## Использование в компонентах

### Через Pinia Store

Рекомендуемый способ - использование через store:

```javascript
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
await authStore.login(username, password)
```

### Прямое использование сервиса

```javascript
import { authService } from '@/services/authService'

const user = await authService.getCurrentUser()
```

## Обработка ошибок

### В Store

```javascript
try {
  const result = await authStore.login(username, password)
  if (result.success) {
    // Успех
  } else {
    // Ошибка: result.error
  }
} catch (error) {
  // Критическая ошибка
}
```

### Прямой вызов API

```javascript
try {
  const response = await api.get('/api/endpoint/')
} catch (error) {
  if (error.response) {
    // Ошибка от сервера
    console.error(error.response.data)
    console.error(error.response.status)
  } else if (error.request) {
    // Запрос отправлен, но ответа нет
    console.error('Network error')
  } else {
    // Ошибка настройки запроса
    console.error('Request setup error')
  }
}
```

## Формат ошибок

Django REST Framework возвращает ошибки в формате:

```json
{
  "field_name": ["Error message 1", "Error message 2"],
  "non_field_errors": ["General error message"]
}
```

Store автоматически парсит эти ошибки и формирует читаемые сообщения.

## Расширение API

Для добавления новых эндпоинтов:

1. Создайте новый сервис в `src/services/` или добавьте методы в существующий
2. Используйте базовый `api` клиент:

```javascript
import api from './api'

export const newService = {
  async getData() {
    const response = await api.get('/api/new-endpoint/')
    return response.data
  },
  
  async createData(data) {
    const response = await api.post('/api/new-endpoint/', data)
    return response.data
  },
}
```

3. Используйте в компонентах или stores

## CORS

Для работы с API необходимо настроить CORS на бэкенде:

- `django-cors-headers` установлен
- `CORS_ALLOW_ALL_ORIGINS = True` (для разработки)
- Или `CORS_ALLOWED_ORIGINS = ['http://localhost:5173']` (для production)

