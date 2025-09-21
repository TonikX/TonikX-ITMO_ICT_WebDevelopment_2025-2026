# Задание 5: Веб-сервер для GET/POST запросов

## Описание задания

Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки `socket` в Python.

## Требования

- Использование библиотеки `socket`
- Обработка GET и POST HTTP-запросов
- Принятие и запись информации о дисциплине и оценке
- Отдача информации обо всех оценках в виде HTML-страницы

## Техническая реализация

### Веб-сервер

```python
import socket
import json
import urllib.parse
from datetime import datetime

class WebServer:
    def __init__(self, host='localhost', port=8081):
        self.host = host
        self.port = port
        self.grades = []  # Хранение оценок в памяти
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        
        while True:
            client_socket, addr = self.server_socket.accept()
            
            try:
                request = client_socket.recv(1024).decode('utf-8')
                self.handle_request(client_socket, request)
            except Exception as e:
                print(f"Ошибка обработки запроса: {e}")
            finally:
                client_socket.close()
    
    def handle_request(self, client_socket, request):
        lines = request.split('\n')
        if not lines:
            return
            
        request_line = lines[0]
        parts = request_line.split()
        if len(parts) >= 3:
            method, path, version = parts[0], parts[1], parts[2]
            
            if method == 'GET' and path == '/':
                self.handle_get_grades(client_socket)
            elif method == 'POST' and path == '/add_grade':
                self.handle_post_grade(client_socket, request)
            else:
                self.send_404(client_socket)
    
    def handle_get_grades(self, client_socket):
        """Обработка GET запроса - отображение всех оценок"""
        html = self.generate_grades_html()
        response = f"""HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: {len(html.encode('utf-8'))}
Connection: close

{html}"""
        client_socket.send(response.encode('utf-8'))
    
    def handle_post_grade(self, client_socket, request):
        """Обработка POST запроса - добавление новой оценки"""
        body_start = request.find('\r\n\r\n')
        if body_start != -1:
            body = request[body_start + 4:]
            data = urllib.parse.parse_qs(body)
            
            discipline = data.get('discipline', [''])[0]
            grade = data.get('grade', [''])[0]
            
            if discipline and grade:
                try:
                    grade_value = int(grade)
                    if 1 <= grade_value <= 5:
                        self.grades.append({
                            'discipline': discipline,
                            'grade': grade_value,
                            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
                        
                        response = """HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Connection: close

{"message": "Оценка добавлена успешно"}"""
                    else:
                        response = """HTTP/1.1 400 Bad Request
Content-Type: application/json; charset=utf-8
Connection: close

{"error": "Оценка должна быть от 1 до 5"}"""
                except ValueError:
                    response = """HTTP/1.1 400 Bad Request
Content-Type: application/json; charset=utf-8
Connection: close

{"error": "Оценка должна быть числом"}"""
            else:
                response = """HTTP/1.1 400 Bad Request
Content-Type: application/json; charset=utf-8
Connection: close

{"error": "Необходимы поля discipline и grade"}"""
        
        client_socket.send(response.encode('utf-8'))
```

## HTML интерфейс

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Система оценок</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        form {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }
        input, button {
            margin: 5px;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        button {
            background-color: #007bff;
            color: white;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Система управления оценками</h1>
        
        <h2>Список оценок</h2>
        <table>
            <tr>
                <th>Дисциплина</th>
                <th>Оценка</th>
                <th>Дата добавления</th>
            </tr>
            <!-- Оценки будут добавлены динамически -->
        </table>
        
        <h2>Добавить оценку</h2>
        <form method="POST" action="/add_grade">
            <p>
                <label for="discipline">Дисциплина:</label><br>
                <input type="text" id="discipline" name="discipline" required>
            </p>
            <p>
                <label for="grade">Оценка:</label><br>
                <input type="number" id="grade" name="grade" min="1" max="5" required>
            </p>
            <p>
                <button type="submit">Добавить оценку</button>
            </p>
        </form>
    </div>
</body>
</html>
```

## HTTP методы

### GET / - Получение всех оценок

**Запрос:**
```
GET / HTTP/1.1
Host: localhost:8081
```

**Ответ:**
```html
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8

<!DOCTYPE html>
<html>
...
</html>
```

### POST /add_grade - Добавление оценки

**Запрос:**
```
POST /add_grade HTTP/1.1
Host: localhost:8081
Content-Type: application/x-www-form-urlencoded

discipline=Математика&grade=5
```

**Ответ:**
```json
HTTP/1.1 200 OK
Content-Type: application/json

{"message": "Оценка добавлена успешно"}
```

## Запуск

### Отдельные компоненты

```bash
# Запуск сервера
python task5_web_server.py server

# Демонстрация
python task5_web_server.py demo
```

### Через главное меню

```bash
python main.py
# Выберите пункт 5
```

## Тестирование

### С помощью curl

```bash
# Получение страницы с оценками
curl http://localhost:8081/

# Добавление новой оценки
curl -X POST http://localhost:8081/add_grade \
  -d "discipline=Физика&grade=4"
```

### С помощью браузера

1. Откройте http://localhost:8081/
2. Заполните форму добавления оценки
3. Нажмите "Добавить оценку"
4. Обновите страницу для просмотра всех оценок