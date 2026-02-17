# test_api_endpoints.py
import requests
import json
from datetime import date, timedelta

BASE_URL = "http://127.0.0.1:8000"
ADMIN_TOKEN = None


def setup():
    """Настройка тестов"""
    global ADMIN_TOKEN

    # Получаем токен админа
    response = requests.post(
        f"{BASE_URL}/auth/token/login/",
        json={"username": "admin", "password": "admin123"}
    )

    if response.status_code == 200:
        ADMIN_TOKEN = response.json()["auth_token"]
        print("✓ Токен админа получен")
        return True

    print("✗ Не удалось получить токен админа")
    return False


def get_headers():
    """Заголовки с токеном"""
    return {
        "Authorization": f"Token {ADMIN_TOKEN}",
        "Content-Type": "application/json"
    }


def test_all_endpoints():
    """Тестируем все endpoint'ы из ТЗ"""

    print("\n" + "=" * 60)
    print("ТЕСТИРОВАНИЕ ВСЕХ ENDPOINT'ОВ ИЗ ТЗ")
    print("=" * 60)

    # 1. Создаем тестовые данные
    print("\n1. Создаем тестовые данные...")

    # Создаем номер
    room_data = {
        "number": "999",
        "floor": 9,
        "room_type": "double",
        "price_per_day": "3000.00",
        "phone": "9999",
        "is_available": True
    }

    response = requests.post(
        f"{BASE_URL}/api/rooms/",
        json=room_data,
        headers=get_headers()
    )

    if response.status_code == 201:
        room_id = response.json()["id"]
        print(f"✓ Создан номер ID: {room_id}")
    else:
        print(f"✗ Ошибка создания номера: {response.text}")
        return

    # Создаем клиента
    client_data = {
        "passport": "9900112233",
        "last_name": "Тестовый",
        "first_name": "Клиент",
        "middle_name": "Тестович",
        "city": "Москва",
        "check_in_date": "2024-11-01",
        "check_out_date": None,
        "room": room_id
    }

    response = requests.post(
        f"{BASE_URL}/api/clients/",
        json=client_data,
        headers=get_headers()
    )

    if response.status_code == 201:
        client_id = response.json()["id"]
        print(f"✓ Создан клиент ID: {client_id}")
    else:
        print(f"✗ Ошибка создания клиента: {response.text}")
        return

    # Создаем сотрудника
    employee_data = {
        "last_name": "Тестовый",
        "first_name": "Сотрудник",
        "middle_name": "Тестович",
        "is_active": True
    }

    response = requests.post(
        f"{BASE_URL}/api/employees/",
        json=employee_data,
        headers=get_headers()
    )

    if response.status_code == 201:
        employee_id = response.json()["id"]
        print(f"✓ Создан сотрудник ID: {employee_id}")
    else:
        print(f"✗ Ошибка создания сотрудника: {response.text}")
        return

    # 2. Тестируем все требования из ТЗ
    print("\n2. Тестируем требования из ТЗ:")
    print("-" * 40)

    # 2.1 Клиенты в номере за период
    print("\nа) Клиенты в номере за период:")
    data = {
        "room_id": room_id,
        "start_date": "2024-10-01",
        "end_date": "2024-12-01"
    }

    response = requests.post(
        f"{BASE_URL}/api/rooms/clients_in_period/",
        json=data,
        headers=get_headers()
    )

    if response.status_code == 200:
        print(f"✓ Найдено клиентов: {len(response.json())}")
    else:
        print(f"✗ Ошибка: {response.text}")

    # 2.2 Количество клиентов из города
    print("\nб) Количество клиентов из города:")
    response = requests.get(
        f"{BASE_URL}/api/clients/from_city/?city=Москва",
        headers=get_headers()
    )

    if response.status_code == 200:
        count = response.json().get("count", 0)
        print(f"✓ Клиентов из Москвы: {count}")
    else:
        print(f"✗ Ошибка: {response.text}")

    # 2.3 Свободные номера
    print("\nв) Свободные номера:")
    response = requests.get(
        f"{BASE_URL}/api/rooms/available/",
        headers=get_headers()
    )

    if response.status_code == 200:
        rooms = response.json()
        print(f"✓ Свободных номеров: {len(rooms)}")
    else:
        print(f"✗ Ошибка: {response.text}")

    # 2.4 Клиенты в тот же период
    print("\nг) Клиенты в тот же период:")
    data = {
        "client_id": client_id,
        "start_date": "2024-10-01",
        "end_date": "2024-12-01"
    }

    response = requests.post(
        f"{BASE_URL}/api/clients/same_period_clients/",
        json=data,
        headers=get_headers()
    )

    if response.status_code == 200:
        print(f"✓ Найдено клиентов: {len(response.json())}")
    else:
        print(f"✗ Ошибка: {response.text}")

    # 2.5 Отчёт за квартал
    print("\nд) Отчёт за квартал:")
    response = requests.get(
        f"{BASE_URL}/api/report/?quarter=4&year=2024",
        headers=get_headers()
    )

    if response.status_code == 200:
        report = response.json()
        print(f"✓ Отчёт за {report['period']}")
        print(f"  Общий доход: {report['total_income']}")
    else:
        print(f"✗ Ошибка: {response.text}")

    # 2.6 Увольнение сотрудника
    print("\nе) Увольнение сотрудника:")
    response = requests.post(
        f"{BASE_URL}/api/employees/{employee_id}/fire/",
        headers=get_headers()
    )

    if response.status_code == 200:
        print(f"✓ Сотрудник уволен: {response.json()}")
    else:
        print(f"✗ Ошибка: {response.text}")

    # 2.7 Наём сотрудника
    print("\nж) Наём сотрудника:")
    response = requests.post(
        f"{BASE_URL}/api/employees/{employee_id}/hire/",
        headers=get_headers()
    )

    if response.status_code == 200:
        print(f"✓ Сотрудник нанят: {response.json()}")
    else:
        print(f"✗ Ошибка: {response.text}")

    # 2.8 Выселение клиента
    print("\nз) Выселение клиента:")
    response = requests.post(
        f"{BASE_URL}/api/clients/{client_id}/check_out/",
        json={"check_out_date": "2024-11-15"},
        headers=get_headers()
    )

    if response.status_code == 200:
        print(f"✓ Клиент выселен: {response.json()}")
    else:
        print(f"✗ Ошибка: {response.text}")

    # 2.9 Общая статистика
    print("\nи) Общая статистика гостиницы:")
    response = requests.get(
        f"{BASE_URL}/api/statistics/hotel/",
        headers=get_headers()
    )

    if response.status_code == 200:
        stats = response.json()
        print(f"✓ Номера: {stats['rooms']['total']} всего, {stats['rooms']['available']} свободно")
    else:
        print(f"✗ Ошибка: {response.text}")

    print("\n" + "=" * 60)
    print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО!")
    print("=" * 60)


if __name__ == "__main__":
    if setup():
        test_all_endpoints()
    else:
        print("Не удалось настроить тесты")