# Аутентификация и авторизация

Подробное руководство по работе с аутентификацией в системе управления читальным залом.

## Технологии

- **Djoser 2.2.3** - библиотека для управления пользователями
- **djangorestframework-simplejwt** - JWT токены
- **Django REST Framework permissions** - права доступа

## JWT токены

Система использует **JWT (JSON Web Tokens)** для аутентификации.

### Типы токенов

1. **Access Token** - кратковременный токен для доступа к API (15 минут)
2. **Refresh Token** - долговременный токен для обновления access токена (1 день)

---

## Регистрация пользователя

### Endpoint

```
POST /api/auth/users/
```

### Request

```json
{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "SecurePass123!",
  "re_password": "SecurePass123!"
}
```

### Response (201 Created)

```json
{
  "email": "newuser@example.com",
  "username": "newuser",
  "id": 1
}
```

### Требования к паролю

- Минимум 8 символов
- Не должен совпадать с именем пользователя
- Не должен быть слишком простым

### Пример (cURL)

```bash
curl -X POST http://localhost:8000/api/auth/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "SecurePass123!",
    "re_password": "SecurePass123!"
  }'
```

---

## Вход в систему (получение токенов)

### Endpoint

```
POST /api/auth/jwt/create/
```

### Request

```json
{
  "username": "newuser",
  "password": "SecurePass123!"
}
```

### Response (200 OK)

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Пример (Python)

```python
import requests

response = requests.post(
    'http://localhost:8000/api/auth/jwt/create/',
    json={
        'username': 'newuser',
        'password': 'SecurePass123!'
    }
)

tokens = response.json()
access_token = tokens['access']
refresh_token = tokens['refresh']

print(f"Access token: {access_token}")
```

---

## Использование токена

После получения access токена, его нужно передавать в заголовке `Authorization` с каждым запросом:

```
Authorization: Bearer <access_token>
```

### Пример (cURL)

```bash
curl http://localhost:8000/api/reading-rooms/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### Пример (Python requests)

```python
import requests

headers = {
    'Authorization': f'Bearer {access_token}'
}

response = requests.get(
    'http://localhost:8000/api/reading-rooms/',
    headers=headers
)

rooms = response.json()
```

### Пример (JavaScript Axios)

```javascript
const axios = require('axios');

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    Authorization: `Bearer ${accessToken}`
  }
});

const { data } = await api.get('/reading-rooms/');
```

---

## Обновление токена

Access токен действителен 15 минут. Для получения нового используйте refresh токен.

### Endpoint

```
POST /api/auth/jwt/refresh/
```

### Request

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Response (200 OK)

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Автоматическое обновление (JavaScript)

```javascript
class APIClient {
  constructor(baseURL) {
    this.baseURL = baseURL;
    this.accessToken = null;
    this.refreshToken = null;
  }

  async login(username, password) {
    const response = await fetch(`${this.baseURL}/auth/jwt/create/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    
    const data = await response.json();
    this.accessToken = data.access;
    this.refreshToken = data.refresh;
    
    return data;
  }

  async refreshAccessToken() {
    const response = await fetch(`${this.baseURL}/auth/jwt/refresh/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh: this.refreshToken })
    });
    
    const data = await response.json();
    this.accessToken = data.access;
    
    return data;
  }

  async request(endpoint, options = {}) {
    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.accessToken}`,
          ...options.headers
        }
      });

      if (response.status === 401) {
        // Token expired, refresh it
        await this.refreshAccessToken();
        
        // Retry request
        return this.request(endpoint, options);
      }

      return response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }
}

// Использование
const api = new APIClient('http://localhost:8000/api');
await api.login('user', 'pass');
const rooms = await api.request('/reading-rooms/');
```

---

## Получение информации о текущем пользователе

### Endpoint

```
GET /api/auth/users/me/
```

### Request

```
Authorization: Bearer <access_token>
```

### Response (200 OK)

```json
{
  "id": 1,
  "username": "newuser",
  "email": "newuser@example.com"
}
```

---

## Права доступа (Permissions)

### Текущая конфигурация

Все авторизованные пользователи имеют полный доступ ко всем операциям:

```python
# reading_room/views.py
class IsAuthenticatedForAll(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
```

### ViewSets с permissions

```python
class ReadingRoomViewSet(viewsets.ModelViewSet):
    queryset = ReadingRoom.objects.all()
    serializer_class = ReadingRoomSerializer
    permission_classes = [IsAuthenticatedForAll]
```

### Доступные permission классы

#### 1. IsAuthenticatedForAll (используется в проекте)

```python
class IsAuthenticatedForAll(permissions.BasePermission):
    """Все операции доступны авторизованным пользователям"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
```

#### 2. IsAdminOrReadOnly (альтернатива)

```python
class IsAdminOrReadOnly(permissions.BasePermission):
    """Админы могут все, остальные только читать"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
```

#### 3. IsOwnerOrReadOnly (альтернатива)

```python
class IsOwnerOrReadOnly(permissions.BasePermission):
    """Редактировать могут только владельцы объекта"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
```

---

## Создание администратора

### Через manage.py

```bash
python manage.py createsuperuser
```

### Через скрипт make_staff.py

```bash
python make_staff.py
# Введите имя пользователя: newuser
```

**Содержимое make_staff.py:**

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def make_user_staff():
    username = input("Введите имя пользователя: ")
    try:
        user = User.objects.get(username=username)
        user.is_staff = True
        user.save()
        print(f"Пользователь '{username}' теперь администратор.")
    except User.DoesNotExist:
        print(f"Пользователь '{username}' не найден.")

if __name__ == "__main__":
    make_user_staff()
```

---

## Настройки JWT (settings.py)

```python
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

DJOSER = {
    'LOGIN_FIELD': 'username',
    'USER_CREATE_PASSWORD_RETYPE': True,
    'SERIALIZERS': {
        'user_create': 'djoser.serializers.UserCreateSerializer',
        'user': 'djoser.serializers.UserSerializer',
        'current_user': 'djoser.serializers.UserSerializer',
    },
}
```

---

## Обработка ошибок аутентификации

### 401 Unauthorized

**Причины:**
- Токен не предоставлен
- Токен недействителен
- Токен истек

**Пример ответа:**

```json
{
  "detail": "Authentication credentials were not provided."
}
```

или

```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```

### Обработка в клиенте

```python
import requests

def api_request(url, token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 401:
        # Token expired, need to refresh or re-login
        print("Токен истек, требуется повторный вход")
        return None
    
    return response.json()
```

---

## Защита маршрутов

### В Django

```python
# views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({'message': 'Доступно только авторизованным'})
```

### Во Vue.js

```javascript
// router/index.js
const router = createRouter({
  routes: [
    {
      path: '/dashboard',
      component: Dashboard,
      meta: { requiresAuth: true }
    }
  ]
});

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login');
  } else {
    next();
  }
});
```

---

## Тестирование аутентификации

### Через Swagger UI

1. Откройте `http://localhost:8000/api/schema/swagger-ui/`
2. Выполните POST `/api/auth/jwt/create/`
3. Скопируйте access токен
4. Нажмите кнопку "Authorize"
5. Введите: `Bearer <ваш_токен>`
6. Теперь все запросы будут авторизованы

### Через pytest

```python
import pytest
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticated_client(api_client):
    # Создаем пользователя
    response = api_client.post('/api/auth/users/', {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123',
        're_password': 'testpass123'
    })
    
    # Получаем токен
    response = api_client.post('/api/auth/jwt/create/', {
        'username': 'testuser',
        'password': 'testpass123'
    })
    
    token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    return api_client

def test_protected_endpoint(authenticated_client):
    response = authenticated_client.get('/api/reading-rooms/')
    assert response.status_code == 200
```

---

## Best Practices

### 1. Хранение токенов

**✅ Правильно:**
- В памяти приложения (для SPA)
- В HttpOnly cookies (для серверного рендеринга)
- В Keychain/Keystore (для мобильных приложений)

**❌ Неправильно:**
- В localStorage (уязвимо к XSS)
- В sessionStorage (то же самое)

### 2. Обновление токенов

```javascript
// Пример правильной реализации
let refreshPromise = null;

async function refreshToken() {
  if (!refreshPromise) {
    refreshPromise = fetch('/api/auth/jwt/refresh/', {
      method: 'POST',
      body: JSON.stringify({ refresh: getRefreshToken() })
    }).then(r => r.json());
  }
  
  try {
    const data = await refreshPromise;
    setAccessToken(data.access);
    return data.access;
  } finally {
    refreshPromise = null;
  }
}
```

### 3. Logout

```javascript
function logout() {
  // Удалить токены
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  
  // Редирект на страницу входа
  router.push('/login');
}
```

