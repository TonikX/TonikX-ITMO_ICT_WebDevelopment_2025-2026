# Тестирование API

Примеры тестирования системы управления читальным залом различными способами.

## Swagger UI (Рекомендуемый способ)

### Открытие Swagger UI

```
http://localhost:8000/api/schema/swagger-ui/
```

### Авторизация в Swagger

1. Найдите раздел **auth** → `/api/auth/jwt/create/`
2. Нажмите "Try it out"
3. Введите данные:
   ```json
   {
     "username": "admin",
     "password": "admin123"
   }
   ```
4. Нажмите "Execute"
5. Скопируйте `access` токен
6. Нажмите кнопку **"Authorize"** вверху страницы
7. Введите: `Bearer <ваш_токен>`
8. Нажмите "Authorize"

### Тестирование endpoints

Теперь можете тестировать любой endpoint:
- Выберите endpoint
- Нажмите "Try it out"
- Заполните параметры
- Нажмите "Execute"
- Просмотрите ответ

---

## Postman

### Импорт OpenAPI схемы

1. Откройте Postman
2. **File** → **Import**
3. Введите URL: `http://localhost:8000/api/schema/`
4. Нажмите **Import**

### Ручное создание запросов

#### 1. Получение токена

**Request:**
```
POST http://localhost:8000/api/auth/jwt/create/
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1Q...",
  "access": "eyJ0eXAiOiJKV1Q..."
}
```

#### 2. Использование токена

Добавьте в Headers:
```
Authorization: Bearer eyJ0eXAiOiJKV1Q...
```

#### 3. Тестирование endpoints

**Список залов:**
```
GET http://localhost:8000/api/reading-rooms/
Authorization: Bearer <token>
```

**Создание зала:**
```
POST http://localhost:8000/api/reading-rooms/
Authorization: Bearer <token>
Content-Type: application/json

{
  "number": 401,
  "floor": 4,
  "room_type": "medium",
  "capacity": 30,
  "hourly_rate": "180.00",
  "description": "Зал с видом на парк"
}
```

---

## cURL (Командная строка)

### Регистрация

```bash
curl -X POST http://localhost:8000/api/auth/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "securepass123",
    "re_password": "securepass123"
  }'
```

### Получение токена

```bash
curl -X POST http://localhost:8000/api/auth/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "password": "securepass123"
  }'
```

**Сохранение токена в переменную (Linux/Mac):**
```bash
TOKEN=$(curl -X POST http://localhost:8000/api/auth/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | jq -r '.access')

echo $TOKEN
```

### CRUD операции

**Список залов:**
```bash
curl http://localhost:8000/api/reading-rooms/ \
  -H "Authorization: Bearer $TOKEN"
```

**Создание зала:**
```bash
curl -X POST http://localhost:8000/api/reading-rooms/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "number": 501,
    "floor": 5,
    "room_type": "large",
    "capacity": 60,
    "hourly_rate": "350.00",
    "description": "Конференц-зал"
  }'
```

**Обновление зала:**
```bash
curl -X PATCH http://localhost:8000/api/reading-rooms/1/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "hourly_rate": "160.00"
  }'
```

**Удаление зала:**
```bash
curl -X DELETE http://localhost:8000/api/reading-rooms/1/ \
  -H "Authorization: Bearer $TOKEN"
```

---

## Python (requests)

### Установка

```bash
pip install requests
```

### Примеры

```python
import requests
import json

BASE_URL = "http://localhost:8000/api"

# 1. Регистрация
response = requests.post(
    f"{BASE_URL}/auth/users/",
    json={
        "username": "pythonuser",
        "email": "python@example.com",
        "password": "pypass123",
        "re_password": "pypass123"
    }
)
print("Регистрация:", response.status_code)

# 2. Получение токена
response = requests.post(
    f"{BASE_URL}/auth/jwt/create/",
    json={
        "username": "pythonuser",
        "password": "pypass123"
    }
)
tokens = response.json()
access_token = tokens['access']
print(f"Access token: {access_token[:20]}...")

# 3. Создание headers с токеном
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# 4. Получение списка залов
response = requests.get(
    f"{BASE_URL}/reading-rooms/",
    headers=headers
)
rooms = response.json()
print(f"Найдено залов: {len(rooms)}")

# 5. Создание зала
new_room = {
    "number": 601,
    "floor": 6,
    "room_type": "small",
    "capacity": 15,
    "hourly_rate": "120.00",
    "description": "Маленький тихий зал"
}
response = requests.post(
    f"{BASE_URL}/reading-rooms/",
    headers=headers,
    json=new_room
)
created_room = response.json()
print(f"Создан зал ID: {created_room['id']}")

# 6. Поиск свободных залов
from datetime import datetime
response = requests.get(
    f"{BASE_URL}/reading-rooms/free/",
    headers=headers,
    params={"on": "2024-11-05T14:00:00"}
)
free_rooms = response.json()
print(f"Свободных залов: {len(free_rooms)}")

# 7. Создание читателя
new_reader = {
    "library_card": "RD2024999",
    "last_name": "Тестов",
    "first_name": "Тест",
    "phone": "+79999999999",
    "email": "test@example.com"
}
response = requests.post(
    f"{BASE_URL}/readers/",
    headers=headers,
    json=new_reader
)
reader = response.json()
print(f"Создан читатель ID: {reader['id']}")

# 8. Создание бронирования
new_reservation = {
    "reader": reader['id'],
    "reading_room": created_room['id'],
    "reserved_from": "2024-11-05T10:00:00Z",
    "reserved_to": "2024-11-05T14:00:00Z",
    "is_active": True
}
response = requests.post(
    f"{BASE_URL}/reservations/",
    headers=headers,
    json=new_reservation
)
reservation = response.json()
print(f"Создано бронирование ID: {reservation['id']}")

# 9. Квартальный отчет
response = requests.get(
    f"{BASE_URL}/reports/quarter/",
    headers=headers,
    params={"quarter": 1}
)
report = response.json()
print(f"Квартальный отчет: доход = {report['total_income']}")
```

---

## JavaScript (Axios)

### Установка

```bash
npm install axios
```

### Примеры

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8000/api';

async function testAPI() {
  try {
    // 1. Регистрация
    await axios.post(`${BASE_URL}/auth/users/`, {
      username: 'jsuser',
      email: 'js@example.com',
      password: 'jspass123',
      re_password: 'jspass123'
    });
    console.log('✅ Регистрация успешна');

    // 2. Получение токена
    const { data: tokens } = await axios.post(`${BASE_URL}/auth/jwt/create/`, {
      username: 'jsuser',
      password: 'jspass123'
    });
    const accessToken = tokens.access;
    console.log('✅ Токен получен');

    // 3. Настройка axios с токеном
    const api = axios.create({
      baseURL: BASE_URL,
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    });

    // 4. Получение списка залов
    const { data: rooms } = await api.get('/reading-rooms/');
    console.log(`✅ Найдено залов: ${rooms.length}`);

    // 5. Создание зала
    const { data: newRoom } = await api.post('/reading-rooms/', {
      number: 701,
      floor: 7,
      room_type: 'medium',
      capacity: 40,
      hourly_rate: '220.00',
      description: 'JavaScript Test Room'
    });
    console.log(`✅ Создан зал ID: ${newRoom.id}`);

    // 6. Обновление зала
    const { data: updatedRoom } = await api.patch(`/reading-rooms/${newRoom.id}/`, {
      hourly_rate: '230.00'
    });
    console.log(`✅ Обновлена цена: ${updatedRoom.hourly_rate}`);

    // 7. Поиск свободных залов
    const { data: freeRooms } = await api.get('/reading-rooms/free/', {
      params: { on: '2024-11-05T14:00:00' }
    });
    console.log(`✅ Свободных залов: ${freeRooms.length}`);

    // 8. Квартальный отчет
    const { data: report } = await api.get('/reports/quarter/', {
      params: { quarter: 1 }
    });
    console.log(`✅ Квартальный доход: ${report.total_income}`);

  } catch (error) {
    console.error('❌ Ошибка:', error.response?.data || error.message);
  }
}

testAPI();
```

---

## Unit тесты (pytest)

### Установка

```bash
pip install pytest pytest-django
```

### Создание тестов

Создайте файл `reading_room/tests.py`:

```python
import pytest
from django.contrib.auth import get_User_model
from rest_framework.test import APIClient
from reading_room.models import ReadingRoom, Reader

User = get_User_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    def make_user(**kwargs):
        return User.objects.create_user(**kwargs)
    return make_user

@pytest.fixture
def authenticated_client(api_client, create_user):
    user = create_user(username='testuser', password='testpass')
    response = api_client.post('/api/auth/jwt/create/', {
        'username': 'testuser',
        'password': 'testpass'
    })
    token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client

@pytest.mark.django_db
class TestReadingRooms:
    def test_create_reading_room(self, authenticated_client):
        response = authenticated_client.post('/api/reading-rooms/', {
            'number': 101,
            'floor': 1,
            'room_type': 'small',
            'capacity': 20,
            'hourly_rate': '150.00'
        })
        assert response.status_code == 201
        assert response.data['number'] == 101
    
    def test_list_reading_rooms(self, authenticated_client):
        ReadingRoom.objects.create(
            number=101, floor=1, room_type='small',
            capacity=20, hourly_rate=150.00
        )
        response = authenticated_client.get('/api/reading-rooms/')
        assert response.status_code == 200
        assert len(response.data) == 1
    
    def test_update_reading_room(self, authenticated_client):
        room = ReadingRoom.objects.create(
            number=101, floor=1, room_type='small',
            capacity=20, hourly_rate=150.00
        )
        response = authenticated_client.patch(f'/api/reading-rooms/{room.id}/', {
            'hourly_rate': '175.00'
        })
        assert response.status_code == 200
        assert response.data['hourly_rate'] == '175.00'
    
    def test_delete_reading_room(self, authenticated_client):
        room = ReadingRoom.objects.create(
            number=101, floor=1, room_type='small',
            capacity=20, hourly_rate=150.00
        )
        response = authenticated_client.delete(f'/api/reading-rooms/{room.id}/')
        assert response.status_code == 204
        assert not ReadingRoom.objects.filter(id=room.id).exists()

@pytest.mark.django_db
class TestReaders:
    def test_create_reader(self, authenticated_client):
        response = authenticated_client.post('/api/readers/', {
            'library_card': 'RD2024001',
            'last_name': 'Тестов',
            'first_name': 'Тест',
            'phone': '+79991234567',
            'email': 'test@example.com'
        })
        assert response.status_code == 201
        assert response.data['library_card'] == 'RD2024001'
```

### Запуск тестов

```bash
# Все тесты
pytest

# С подробным выводом
pytest -v

# Конкретный файл
pytest reading_room/tests.py

# Конкретный тест
pytest reading_room/tests.py::TestReadingRooms::test_create_reading_room

# С покрытием
pytest --cov=reading_room
```

---

## Сценарии тестирования

### Сценарий 1: Создание и бронирование зала

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Получение токена
response = requests.post(f"{BASE_URL}/auth/jwt/create/", 
    json={"username": "admin", "password": "admin123"})
token = response.json()['access']
headers = {"Authorization": f"Bearer {token}"}

# 1. Создать зал
room = requests.post(f"{BASE_URL}/reading-rooms/", 
    headers=headers,
    json={
        "number": 101,
        "floor": 1,
        "room_type": "small",
        "capacity": 20,
        "hourly_rate": "150.00"
    }).json()

# 2. Создать читателя
reader = requests.post(f"{BASE_URL}/readers/", 
    headers=headers,
    json={
        "library_card": "RD2024001",
        "last_name": "Иванов",
        "first_name": "Иван",
        "phone": "+79991234567"
    }).json()

# 3. Создать бронирование
reservation = requests.post(f"{BASE_URL}/reservations/", 
    headers=headers,
    json={
        "reader": reader['id'],
        "reading_room": room['id'],
        "reserved_from": "2024-11-05T10:00:00Z",
        "reserved_to": "2024-11-05T14:00:00Z",
        "is_active": True
    }).json()

print(f"✅ Зал {room['number']} забронирован на {reader['last_name']}")
```

### Сценарий 2: Поиск свободных залов

```python
# Проверка свободных залов на конкретное время
free_rooms = requests.get(
    f"{BASE_URL}/reading-rooms/free/",
    headers=headers,
    params={"on": "2024-11-05T14:00:00"}
).json()

for room in free_rooms:
    print(f"Свободен зал №{room['number']}, этаж {room['floor']}, {room['capacity']} мест")
```

### Сценарий 3: Генерация отчета

```python
# Получение квартального отчета
report = requests.get(
    f"{BASE_URL}/reports/quarter/",
    headers=headers,
    params={"quarter": 1}
).json()

print(f"Квартал {report['quarter']}")
print(f"Общий доход: {report['total_income']} ₽")
for stat in report['rooms_stats']:
    print(f"  Зал {stat['room_number']}: {stat['income']} ₽")
```

---

## Performance тестирование

### Apache Bench (ab)

```bash
# 100 запросов, 10 одновременных
ab -n 100 -c 10 -H "Authorization: Bearer <token>" \
   http://localhost:8000/api/reading-rooms/
```

### Locust (Python)

```python
from locust import HttpUser, task, between

class ReadingRoomUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        response = self.client.post("/api/auth/jwt/create/", json={
            "username": "admin",
            "password": "admin123"
        })
        self.token = response.json()['access']
        self.client.headers.update({
            'Authorization': f'Bearer {self.token}'
        })
    
    @task
    def list_rooms(self):
        self.client.get("/api/reading-rooms/")
    
    @task
    def list_readers(self):
        self.client.get("/api/readers/")
```

Запуск:
```bash
locust -f locustfile.py
# Откройте http://localhost:8089
```

---

## Итоговая проверка

### Checklist тестирования

- [ ] Регистрация пользователя работает
- [ ] Получение JWT токена работает
- [ ] CRUD для читальных залов работает
- [ ] CRUD для читателей работает
- [ ] CRUD для бронирований работает
- [ ] CRUD для библиотекарей работает
- [ ] Поиск свободных залов работает
- [ ] Квартальные отчеты генерируются
- [ ] Custom endpoints работают
- [ ] Swagger UI доступен и функционален

---

## Заключение

Система протестирована и готова к использованию! 🎉

Переходите к [Лабораторной №4 (Vue.js)](../lab4/index.md) для работы с фронтендом.
