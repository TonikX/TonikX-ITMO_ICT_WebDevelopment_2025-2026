# Примеры запросов

Здесь собраны примеры типичных сценариев использования API.

## Сценарий 1: Регистрация капитана и создание команды

### Шаг 1: Регистрация капитана

```bash
curl -X POST http://localhost:8000/api/auth/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "captain1",
    "email": "captain1@example.com",
    "password": "securepass123",
    "password_retype": "securepass123",
    "first_name": "Иван",
    "last_name": "Иванов",
    "role": "captain"
  }'
```

### Шаг 2: Получение токена

```bash
curl -X POST http://localhost:8000/api/auth/token/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "captain1@example.com",
    "password": "securepass123"
  }'
```

Ответ:
```json
{
  "auth_token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

### Шаг 3: Создание команды

```bash
curl -X POST http://localhost:8000/api/teams/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -d '{
    "name": "Команда Победителей",
    "motto": "Мы лучшие!"
  }'
```

### Шаг 4: Добавление участников

```bash
curl -X POST http://localhost:8000/api/teams/1/add_member/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -d '{
    "first_name": "Петр",
    "last_name": "Петров",
    "email": "petr@example.com"
  }'
```

### Шаг 5: Выбор задачи

```bash
curl -X PATCH http://localhost:8000/api/teams/1/select_task/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -d '{
    "task_id": 1
  }'
```

## Сценарий 2: Работа куратора с задачей

### Шаг 1: Регистрация куратора (через админа)

Куратор должен быть создан главным администратором или через Django Admin.

### Шаг 2: Добавление файла к задаче

```bash
curl -X POST http://localhost:8000/api/tasks/1/add_file/ \
  -H "Authorization: Token <curator_token>" \
  -F "task=1" \
  -F "file=@requirements.pdf" \
  -F "name=Требования к проекту"
```

### Шаг 3: Добавление ссылки

```bash
curl -X POST http://localhost:8000/api/tasks/1/add_link/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <curator_token>" \
  -d '{
    "url": "https://example.com/docs",
    "title": "Документация API"
  }'
```

### Шаг 4: Установка ссылки на консультацию

```bash
curl -X PATCH http://localhost:8000/api/tasks/1/set_consultation_link/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <curator_token>" \
  -d '{
    "consultation_link": "https://zoom.us/j/123456789"
  }'
```

## Сценарий 3: Отправка решения капитаном

### Шаг 1: Создание решения

```bash
curl -X POST http://localhost:8000/api/solutions/ \
  -H "Authorization: Token <captain_token>" \
  -F "task=1" \
  -F "description=Описание нашего решения" \
  -F "file=@solution.zip"
```

### Шаг 2: Просмотр своего решения

```bash
curl -X GET http://localhost:8000/api/solutions/1/ \
  -H "Authorization: Token <captain_token>"
```

## Сценарий 4: Оценка решения жюри

### Шаг 1: Просмотр всех решений

```bash
curl -X GET http://localhost:8000/api/solutions/ \
  -H "Authorization: Token <jury_token>"
```

### Шаг 2: Просмотр решений, отсортированных по дате

```bash
curl -X GET http://localhost:8000/api/evaluations/solutions_by_date/ \
  -H "Authorization: Token <jury_token>"
```

### Шаг 3: Создание оценки

```bash
curl -X POST http://localhost:8000/api/evaluations/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <jury_token>" \
  -d '{
    "solution": 1,
    "score": 9,
    "comment": "Отличное решение! Очень понравился подход к реализации и качество кода."
  }'
```

### Шаг 4: Просмотр своих оценок

```bash
curl -X GET http://localhost:8000/api/evaluations/my_evaluations/ \
  -H "Authorization: Token <jury_token>"
```

## Сценарий 5: Работа главного администратора

### Шаг 1: Создание задачи

```bash
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <admin_token>" \
  -d '{
    "title": "Разработка веб-приложения",
    "description": "Создать современное веб-приложение с использованием React и Django"
  }'
```

### Шаг 2: Назначение куратора

```bash
curl -X PATCH http://localhost:8000/api/tasks/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <admin_token>" \
  -d '{
    "curator": 2
  }'
```

### Шаг 3: Просмотр всех команд

```bash
curl -X GET http://localhost:8000/api/teams/ \
  -H "Authorization: Token <admin_token>"
```

## Примеры с использованием Python (requests)

### Регистрация и получение токена

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Регистрация
response = requests.post(f"{BASE_URL}/auth/users/", json={
    "username": "captain1",
    "email": "captain1@example.com",
    "password": "securepass123",
    "password_retype": "securepass123",
    "role": "captain"
})
print(response.json())

# Получение токена
response = requests.post(f"{BASE_URL}/auth/token/login/", json={
    "email": "captain1@example.com",
    "password": "securepass123"
})
token = response.json()["auth_token"]
print(f"Token: {token}")

# Использование токена
headers = {"Authorization": f"Token {token}"}
response = requests.get(f"{BASE_URL}/teams/", headers=headers)
print(response.json())
```

### Создание команды и отправка решения

```python
import requests

BASE_URL = "http://localhost:8000/api"
token = "your_token_here"
headers = {"Authorization": f"Token {token}"}

# Создание команды
response = requests.post(
    f"{BASE_URL}/teams/",
    headers=headers,
    json={
        "name": "Команда Победителей",
        "motto": "Мы лучшие!"
    }
)
team_id = response.json()["id"]
print(f"Team created: {team_id}")

# Выбор задачи
requests.patch(
    f"{BASE_URL}/teams/{team_id}/select_task/",
    headers=headers,
    json={"task_id": 1}
)

# Отправка решения
with open("solution.zip", "rb") as f:
    files = {"file": f}
    data = {
        "task": 1,
        "description": "Описание решения"
    }
    response = requests.post(
        f"{BASE_URL}/solutions/",
        headers=headers,
        files=files,
        data=data
    )
    print(response.json())
```

## Обработка ошибок

### Пример обработки ошибок в Python

```python
import requests

def make_request(method, url, **kwargs):
    try:
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            print("Ошибка аутентификации. Проверьте токен.")
        elif response.status_code == 403:
            print("Недостаточно прав доступа.")
        elif response.status_code == 404:
            print("Ресурс не найден.")
        else:
            print(f"Ошибка {response.status_code}: {response.text}")
        raise
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
        raise

# Использование
token = "your_token"
headers = {"Authorization": f"Token {token}"}
result = make_request("GET", f"{BASE_URL}/teams/", headers=headers)
```

## Тестирование с помощью Postman

1. **Создайте коллекцию** "Hackathon API"

2. **Добавьте переменные:**
   - `base_url`: `http://localhost:8000/api`
   - `token`: (будет установлен после логина)

3. **Создайте запрос для получения токена:**
   - Method: POST
   - URL: `{{base_url}}/auth/token/login/`
   - Body (raw JSON):
   ```json
   {
     "email": "captain1@example.com",
     "password": "securepass123"
   }
   ```
   - Tests (для автоматического сохранения токена):
   ```javascript
   if (pm.response.code === 200) {
       var jsonData = pm.response.json();
       pm.environment.set("token", jsonData.auth_token);
   }
   ```

4. **Используйте токен в других запросах:**
   - Headers:
     - Key: `Authorization`
     - Value: `Token {{token}}`
