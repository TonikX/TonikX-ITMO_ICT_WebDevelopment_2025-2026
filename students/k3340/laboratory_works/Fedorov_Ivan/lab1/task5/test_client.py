import requests
import json


def test_server():
    base_url = "http://localhost:8080"

    print("Тестирование сервера оценок...")

    try:
        # Тест главной страницы
        response = requests.get(f"{base_url}/")
        print(f"GET / - Status: {response.status_code}")

        # Тест добавления оценок
        test_grades = [
            {"discipline": "Математика", "grade": "5"},
            {"discipline": "Физика", "grade": "4"},
            {"discipline": "Программирование", "grade": "5"},
            {"discipline": "Математика", "grade": "4"},
        ]

        for grade in test_grades:
            response = requests.post(f"{base_url}/add", data=grade)
            print(f"POST /add {grade} - Status: {response.status_code}")

        # Тест JSON API
        response = requests.get(f"{base_url}/api/grades")
        print(f"GET /api/grades - Status: {response.status_code}")
        grades_data = response.json()
        print("Данные оценок:", json.dumps(grades_data, ensure_ascii=False, indent=2))

    except requests.ConnectionError:
        print("Ошибка: не удалось подключиться к серверу. Убедитесь, что сервер запущен.")
    except Exception as e:
        print(f"Ошибка тестирования: {e}")


if __name__ == "__main__":
    test_server()