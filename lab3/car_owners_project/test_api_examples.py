#!/usr/bin/env python
"""
Примеры тестирования API
"""
import requests
import json

BASE_URL = "http://localhost:8000/warriors"

def test_skills_api():
    """Тестирование API навыков"""
    print("=== Тестирование API навыков ===")
    
    # GET - получить все навыки
    response = requests.get(f"{BASE_URL}/skills/")
    print(f"GET /skills/ - Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Количество навыков: {len(data.get('Skills', []))}")
        print("Первые 3 навыка:")
        for skill in data.get('Skills', [])[:3]:
            print(f"  - {skill['title']}")
    
    # POST - создать новый навык
    new_skill = {"skill": {"title": "FastAPI"}}
    response = requests.post(f"{BASE_URL}/skills/", json=new_skill)
    print(f"\nPOST /skills/ - Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Ответ: {response.json()}")


def test_warriors_api():
    """Тестирование API воинов"""
    print("\n=== Тестирование API воинов ===")
    
    # GET - получить всех воинов
    response = requests.get(f"{BASE_URL}/warriors/")
    print(f"GET /warriors/ - Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Количество воинов: {len(data.get('Warriors', []))}")
    
    # GET - получить воинов с профессиями
    response = requests.get(f"{BASE_URL}/warriors/with_profession/")
    print(f"\nGET /warriors/with_profession/ - Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Количество воинов с профессиями: {len(data.get('results', []))}")
        if data.get('results'):
            warrior = data['results'][0]
            print(f"Первый воин: {warrior['name']}")
            if warrior.get('profession'):
                print(f"  Профессия: {warrior['profession']['title']}")
    
    # GET - получить воинов со скиллами
    response = requests.get(f"{BASE_URL}/warriors/with_skills/")
    print(f"\nGET /warriors/with_skills/ - Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Количество воинов со скиллами: {len(data.get('results', []))}")
        if data.get('results'):
            warrior = data['results'][0]
            print(f"Первый воин: {warrior['name']}")
            print(f"  Количество навыков: {len(warrior.get('skill', []))}")
    
    # GET - получить конкретного воина
    response = requests.get(f"{BASE_URL}/warriors/1/")
    print(f"\nGET /warriors/1/ - Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Воин: {data['name']}")
        print(f"  Раса: {data['race']}")
        print(f"  Уровень: {data['level']}")
        if data.get('profession'):
            print(f"  Профессия: {data['profession']['title']}")
        print(f"  Количество навыков: {len(data.get('skill', []))}")


def test_professions_api():
    """Тестирование API профессий"""
    print("\n=== Тестирование API профессий ===")
    
    # POST - создать новую профессию (APIView)
    new_profession = {"profession": {"title": "Frontend Developer", "description": "Разработка пользовательского интерфейса"}}
    response = requests.post(f"{BASE_URL}/profession/create/", json=new_profession)
    print(f"POST /profession/create/ - Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Ответ: {response.json()}")
    
    # POST - создать новую профессию (Generic API View)
    new_profession_generic = {"title": "Backend Developer", "description": "Разработка серверной части"}
    response = requests.post(f"{BASE_URL}/profession/generic_create/", json=new_profession_generic)
    print(f"\nPOST /profession/generic_create/ - Status: {response.status_code}")
    if response.status_code == 201:
        print(f"Ответ: {response.json()}")


def test_warrior_crud():
    """Тестирование CRUD операций с воинами"""
    print("\n=== Тестирование CRUD операций с воинами ===")
    
    # POST - создать нового воина
    new_warrior = {
        "race": "d",
        "name": "Тестовый Воин",
        "level": 5,
        "profession": 1
    }
    response = requests.post(f"{BASE_URL}/warriors/create/", json=new_warrior)
    print(f"POST /warriors/create/ - Status: {response.status_code}")
    if response.status_code == 201:
        data = response.json()
        print(f"Создан воин: {data}")
        warrior_id = data.get('id')
        
        if warrior_id:
            # GET - получить созданного воина
            response = requests.get(f"{BASE_URL}/warriors/{warrior_id}/")
            print(f"\nGET /warriors/{warrior_id}/ - Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Воин: {data['name']} (ID: {data['id']})")
            
            # PUT - обновить воина
            updated_warrior = {
                "race": "t",
                "name": "Обновленный Воин",
                "level": 8,
                "profession": 2
            }
            response = requests.put(f"{BASE_URL}/warriors/{warrior_id}/update/", json=updated_warrior)
            print(f"\nPUT /warriors/{warrior_id}/update/ - Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Обновлен воин: {data['name']} (уровень: {data['level']})")
            
            # DELETE - удалить воина
            response = requests.delete(f"{BASE_URL}/warriors/{warrior_id}/delete/")
            print(f"\nDELETE /warriors/{warrior_id}/delete/ - Status: {response.status_code}")
            if response.status_code == 204:
                print("Воин успешно удален")


def main():
    """Основная функция тестирования"""
    print("Запуск тестирования Django REST Framework API")
    print("=" * 50)
    
    try:
        # Проверяем доступность сервера
        response = requests.get(f"{BASE_URL}/warriors/")
        if response.status_code != 200:
            print("Ошибка: Сервер недоступен. Убедитесь, что Django сервер запущен.")
            return
        
        # Запускаем тесты
        test_skills_api()
        test_warriors_api()
        test_professions_api()
        test_warrior_crud()
        
        print("\n" + "=" * 50)
        print("Тестирование завершено!")
        
    except requests.exceptions.ConnectionError:
        print("Ошибка: Не удается подключиться к серверу.")
        print("Убедитесь, что Django сервер запущен на http://localhost:8000")
    except Exception as e:
        print(f"Ошибка при тестировании: {e}")


if __name__ == "__main__":
    main()
