"""
Тестирование API endpoints
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8001/war"


def print_section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def test_endpoint(name, url, method="GET", data=None):
    print(f"\n{name}")
    print(f"URL: {url}")
    print(f"Метод: {method}")

    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(
                url, json=data, headers={"Content-Type": "application/json"}
            )
        elif method == "DELETE":
            response = requests.delete(url)

        print(f"Статус: {response.status_code}")

        if response.status_code in [200, 201]:
            result = response.json()
            print("Ответ:")
            print(json.dumps(result, indent=2, ensure_ascii=False)[:500])
            return True
        else:
            print(f"Ошибка: {response.text}")
            return False
    except Exception as e:
        print(f"Ошибка: {e}")
        return False


# Тестирование APIView endpoints
print_section("ТЕСТИРОВАНИЕ APIView ENDPOINTS")

test_endpoint("1. Просмотр всех воинов (APIView)", f"{BASE_URL}/api/warriors/")

test_endpoint(
    "2. Просмотр всех умений (APIView) - Задание 1", f"{BASE_URL}/api/skills/"
)

# Тестирование Generic Views endpoints
print_section("ТЕСТИРОВАНИЕ GENERIC VIEWS ENDPOINTS")

test_endpoint("3. Список воинов (Generic View)", f"{BASE_URL}/warriors/list/")

test_endpoint("4. Список умений (Generic View)", f"{BASE_URL}/skills/list/")

# Тестирование практического задания 2
print_section("ПРАКТИЧЕСКОЕ ЗАДАНИЕ 2: ВЛОЖЕННЫЕ ДАННЫЕ")

test_endpoint(
    "5. Воины с профессиями (Задание 2.1)", f"{BASE_URL}/warriors/with-professions/"
)

test_endpoint("6. Воины с умениями (Задание 2.2)", f"{BASE_URL}/warriors/with-skills/")

test_endpoint(
    "7. Детальная информация о воине (Задание 2.3)", f"{BASE_URL}/warriors/1/"
)

print_section("СОЗДАНИЕ ДАННЫХ")

test_endpoint(
    "8. Создание нового умения (APIView)",
    f"{BASE_URL}/api/skills/create/",
    method="POST",
    data={"skill": {"title": "TypeScript"}},
)

test_endpoint(
    "9. Создание профессии (APIView)",
    f"{BASE_URL}/api/profession/create/",
    method="POST",
    data={
        "profession": {
            "title": "Data Scientist",
            "description": "Специалист по анализу данных",
        }
    },
)

print("\n" + "=" * 70)
print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
print("=" * 70)
print("\nДля просмотра полного функционала откройте в браузере:")
print("http://127.0.0.1:8001/war/warriors/with-professions/")
print("http://127.0.0.1:8001/war/warriors/with-skills/")
print("http://127.0.0.1:8001/war/warriors/1/")
