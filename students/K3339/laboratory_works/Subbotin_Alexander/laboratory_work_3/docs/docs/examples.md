# Примеры использования

Практические примеры работы с Tour Agency API.

## Полный сценарий использования

```python
import requests
from datetime import date, timedelta

BASE_URL = "http://localhost:8000"

# ========== 1. РЕГИСТРАЦИЯ И АВТОРИЗАЦИЯ ==========

# Регистрация нового пользователя
register_data = {
    "username": "traveler_alex",
    "email": "alex@example.com",
    "password": "secure_pass_123"
}

response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
user = response.json()
print(f"✅ Пользователь зарегистрирован: {user['username']}")

# Авторизация
login_data = {
    "username": "traveler_alex",
    "password": "secure_pass_123"
}

response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print(f"✅ Получен токен: {token[:20]}...")

# Обновление профиля
profile_data = {"date_of_birth": "1990-05-15"}
requests.put(f"{BASE_URL}/auth/me/profile", headers=headers, json=profile_data)
print("✅ Профиль обновлён")

# ========== 2. РАБОТА С ТУРАМИ ==========

# Создание нескольких туров
tours_data = [
    {
        "title": "Романтический Париж",
        "agency": "Dream Travel",
        "description": "7 дней в столице Франции",
        "start_date": str(date.today() + timedelta(days=30)),
        "end_date": str(date.today() + timedelta(days=37)),
        "price": 1500.00,
        "city": "Париж",
        "payment_terms": "50% предоплата"
    },
    {
        "title": "Исторический Рим",
        "agency": "Italia Tours",
        "description": "5 дней среди древних руин",
        "start_date": str(date.today() + timedelta(days=60)),
        "end_date": str(date.today() + timedelta(days=65)),
        "price": 1200.00,
        "city": "Рим",
        "payment_terms": "Полная оплата за 14 дней"
    },
    {
        "title": "Современный Токио",
        "agency": "Asia Adventures",
        "description": "10 дней в Японии",
        "start_date": str(date.today() + timedelta(days=90)),
        "end_date": str(date.today() + timedelta(days=100)),
        "price": 2500.00,
        "city": "Токио",
        "payment_terms": "Полная оплата за месяц"
    }
]

tour_ids = []
for tour_data in tours_data:
    response = requests.post(f"{BASE_URL}/tours/", headers=headers, json=tour_data)
    tour = response.json()
    tour_ids.append(tour["id"])
    print(f"✅ Создан тур: {tour['title']} (ID: {tour['id']})")

# Получение списка всех туров
tours = requests.get(f"{BASE_URL}/tours/").json()
print(f"\n📋 Всего туров в системе: {len(tours)}")

# Поиск туров по городу
paris_tours = requests.get(f"{BASE_URL}/tours/", params={"city": "Париж"}).json()
print(f"🗼 Туров в Париже: {len(paris_tours)}")

# ========== 3. БРОНИРОВАНИЕ ==========

# Бронирование первого тура
reservation_data = {
    "tour_id": tour_ids[0],
    "guests": 2,
    "notes": "Нужен номер с видом на Эйфелеву башню"
}

response = requests.post(f"{BASE_URL}/reservations/", headers=headers, json=reservation_data)
reservation = response.json()
reservation_id = reservation["id"]
print(f"\n✅ Создано бронирование #{reservation_id}")
print(f"   Тур: {reservation['tour']['title']}")
print(f"   Гостей: {reservation['guests']}")

# Получение своих бронирований
my_reservations = requests.get(f"{BASE_URL}/reservations/my", headers=headers).json()
print(f"\n📅 Моих бронирований: {len(my_reservations)}")

# Обновление бронирования
update_data = {"guests": 3, "confirmed": True}
requests.put(f"{BASE_URL}/reservations/{reservation_id}", headers=headers, json=update_data)
print(f"✅ Бронирование обновлено: теперь 3 гостя, подтверждено")

# ========== 4. ОТЗЫВЫ ==========

# Написание отзыва на тур
review_data = {
    "tour_id": tour_ids[0],
    "text": "Отличный тур! Всё было организовано на высшем уровне. Особенно понравился отель и экскурсии.",
    "rating": 9
}

response = requests.post(f"{BASE_URL}/reviews/", headers=headers, json=review_data)
review = response.json()
print(f"\n✅ Отзыв опубликован с оценкой {review['rating']}/10")

# Получение всех отзывов на тур
tour_reviews = requests.get(f"{BASE_URL}/reviews/tour/{tour_ids[0]}").json()
print(f"⭐ Отзывов на тур: {len(tour_reviews)}")

# ========== 5. СТАТИСТИКА ==========

# Подсчёт общей стоимости бронирований
total_cost = sum(
    float(res['tour']['price']) * res['guests'] 
    for res in my_reservations
)
print(f"\n💰 Общая стоимость бронирований: ${total_cost:.2f}")

# Средний рейтинг тура
if tour_reviews:
    avg_rating = sum(r['rating'] for r in tour_reviews) / len(tour_reviews)
    print(f"📊 Средний рейтинг тура: {avg_rating:.1f}/10")

print("\n✨ Все операции выполнены успешно!")
```

---

## Работа с ошибками

```python
import requests

BASE_URL = "http://localhost:8000"

def safe_request(method, url, **kwargs):
    """Безопасное выполнение запроса с обработкой ошибок"""
    try:
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json() if response.content else None
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP ошибка: {e.response.status_code}")
        if e.response.content:
            print(f"   Детали: {e.response.json()}")
        return None
    except requests.exceptions.ConnectionError:
        print(f"❌ Ошибка подключения к {url}")
        return None
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        return None

# Попытка создать тур без авторизации
result = safe_request(
    "POST",
    f"{BASE_URL}/tours/",
    json={"title": "Test Tour"}
)
# Вывод: ❌ HTTP ошибка: 401

# Попытка получить несуществующий тур
result = safe_request("GET", f"{BASE_URL}/tours/99999")
# Вывод: ❌ HTTP ошибка: 404
```

---

## Пагинация больших списков

```python
def get_all_tours(base_url, city=None, page_size=20):
    """Получение всех туров с пагинацией"""
    all_tours = []
    offset = 0
    
    while True:
        params = {"limit": page_size, "offset": offset}
        if city:
            params["city"] = city
            
        response = requests.get(f"{base_url}/tours/", params=params)
        tours = response.json()
        
        if not tours:
            break
            
        all_tours.extend(tours)
        print(f"Загружено {len(all_tours)} туров...")
        
        if len(tours) < page_size:
            break
            
        offset += page_size
    
    return all_tours

# Использование
all_tours = get_all_tours(BASE_URL, city="Париж")
print(f"Всего найдено туров в Париже: {len(all_tours)}")
```

---

## Асинхронные запросы (aiohttp)

```python
import aiohttp
import asyncio

async def fetch_tours_async(session, url):
    """Асинхронное получение туров"""
    async with session.get(url) as response:
        return await response.json()

async def main():
    BASE_URL = "http://localhost:8000"
    
    async with aiohttp.ClientSession() as session:
        # Параллельное получение разных данных
        tasks = [
            fetch_tours_async(session, f"{BASE_URL}/tours/?city=Париж"),
            fetch_tours_async(session, f"{BASE_URL}/tours/?city=Рим"),
            fetch_tours_async(session, f"{BASE_URL}/tours/?city=Токио"),
        ]
        
        results = await asyncio.gather(*tasks)
        
        for i, city in enumerate(["Париж", "Рим", "Токио"]):
            print(f"{city}: {len(results[i])} туров")

# Запуск
asyncio.run(main())
```

---

## Класс-обёртка для API

```python
class TourAgencyClient:
    """Удобная обёртка для работы с Tour Agency API"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.token = None
        self.session = requests.Session()
    
    def register(self, username, email, password):
        """Регистрация пользователя"""
        response = self.session.post(
            f"{self.base_url}/auth/register",
            json={"username": username, "email": email, "password": password}
        )
        response.raise_for_status()
        return response.json()
    
    def login(self, username, password):
        """Авторизация и сохранение токена"""
        response = self.session.post(
            f"{self.base_url}/auth/login",
            data={"username": username, "password": password}
        )
        response.raise_for_status()
        self.token = response.json()["access_token"]
        self.session.headers.update({"Authorization": f"Bearer {self.token}"})
        return self.token
    
    def get_tours(self, city=None, limit=100, offset=0):
        """Получение списка туров"""
        params = {"limit": limit, "offset": offset}
        if city:
            params["city"] = city
        response = self.session.get(f"{self.base_url}/tours/", params=params)
        response.raise_for_status()
        return response.json()
    
    def create_reservation(self, tour_id, guests, notes=""):
        """Создание бронирования"""
        response = self.session.post(
            f"{self.base_url}/reservations/",
            json={"tour_id": tour_id, "guests": guests, "notes": notes}
        )
        response.raise_for_status()
        return response.json()
    
    def add_review(self, tour_id, text, rating):
        """Добавление отзыва"""
        response = self.session.post(
            f"{self.base_url}/reviews/",
            json={"tour_id": tour_id, "text": text, "rating": rating}
        )
        response.raise_for_status()
        return response.json()

# Использование
client = TourAgencyClient()
client.register("user123", "user@example.com", "password123")
client.login("user123", "password123")

tours = client.get_tours(city="Париж")
print(f"Найдено туров: {len(tours)}")

if tours:
    reservation = client.create_reservation(tours[0]["id"], guests=2)
    print(f"Создано бронирование #{reservation['id']}")
    
    review = client.add_review(tours[0]["id"], "Отличный тур!", 10)
    print(f"Добавлен отзыв с оценкой {review['rating']}")
```

---

## Тестирование API с pytest

```python
import pytest
import requests

BASE_URL = "http://localhost:8000"

@pytest.fixture
def api_token():
    """Фикстура для получения токена авторизации"""
    # Регистрация
    username = f"testuser_{pytest.timestamp}"
    requests.post(
        f"{BASE_URL}/auth/register",
        json={
            "username": username,
            "email": f"{username}@test.com",
            "password": "testpass123"
        }
    )
    
    # Авторизация
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": username, "password": "testpass123"}
    )
    return response.json()["access_token"]

def test_get_tours():
    """Тест получения списка туров"""
    response = requests.get(f"{BASE_URL}/tours/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_tour(api_token):
    """Тест создания тура"""
    headers = {"Authorization": f"Bearer {api_token}"}
    tour_data = {
        "title": "Test Tour",
        "agency": "Test Agency",
        "description": "Test Description",
        "start_date": "2025-06-01",
        "end_date": "2025-06-07",
        "price": 1000.00,
        "city": "Test City"
    }
    
    response = requests.post(
        f"{BASE_URL}/tours/",
        headers=headers,
        json=tour_data
    )
    
    assert response.status_code == 201
    tour = response.json()
    assert tour["title"] == "Test Tour"
    assert tour["price"] == "1000.00"

def test_unauthorized_access():
    """Тест доступа без авторизации"""
    response = requests.post(
        f"{BASE_URL}/tours/",
        json={"title": "Test"}
    )
    assert response.status_code == 401
```

---

## Экспорт данных

```python
import csv
import json

def export_tours_to_csv(tours, filename="tours.csv"):
    """Экспорт туров в CSV"""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=tours[0].keys())
        writer.writeheader()
        writer.writerows(tours)
    print(f"✅ Экспортировано {len(tours)} туров в {filename}")

def export_tours_to_json(tours, filename="tours.json"):
    """Экспорт туров в JSON"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(tours, f, ensure_ascii=False, indent=2)
    print(f"✅ Экспортировано {len(tours)} туров в {filename}")

# Использование
tours = requests.get(f"{BASE_URL}/tours/").json()
export_tours_to_csv(tours)
export_tours_to_json(tours)
```

Эти примеры покрывают основные сценарии использования Tour Agency API!
