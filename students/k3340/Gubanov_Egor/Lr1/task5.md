# Задание 5: Веб-сервер с Оценками

## Практическое задание

Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.

### Задание:
Сервер должен:
1. Принять и записать информацию о дисциплине и оценке по дисциплине
2. Отдать информацию обо всех оценках по дисциплинам в виде HTML-страницы

### Полезные ссылки:
- [Базовый класс для веб-сервера](https://docs.python.org/3/library/http.server.html)
- [Мануал по созданию сервера](https://python-scripts.com/sockets)

---

## Реализация

### Сервер (task5/server.py)

```python
import socket
import threading
import urllib.parse
import json
import os
import html
from datetime import datetime, timezone

HOST = '127.0.0.1'
PORT = 8005
ENCODING = 'utf-8'
DATA_FILE = 'grades.json'
LOCK = threading.Lock()
SERVER_NAME = 'SimpleGradesServer/1.0'

def load_data():
    """Загружает данные из JSON файла"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_data(data):
    """Сохраняет данные в JSON файл"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def render_page(data):
    """Создает HTML страницу с таблицей оценок"""
    # Группируем оценки по предметам
    subjects = {}
    for item in data:
        subject = item['subject']
        grade = item['grade']
        if subject not in subjects:
            subjects[subject] = []
        subjects[subject].append(grade)
    
    # Генерируем строки таблицы - каждый предмет в отдельной строке
    if subjects:
        rows = ""
        for subject, grades in subjects.items():
            grades_str = ", ".join(grades)
            rows += f"<tr><td>{html.escape(subject)}</td><td>{html.escape(grades_str)}</td></tr>\n"
    else:
        rows = '<tr><td colspan="2" style="text-align: center; color: #999;">Пока нет оценок</td></tr>\n'
    
    # Подсчитываем статистику
    total_grades = len(data)
    avg_grade = sum(int(item['grade']) for item in data if item['grade'].isdigit()) / total_grades if total_grades > 0 else 0

    with open('template.html', 'r', encoding='utf-8') as f:
        template = f.read()

    # Заменяем плейсхолдеры вручную, чтобы избежать конфликтов с CSS
    html_content = template.replace('{total_grades}', str(total_grades))
    html_content = html_content.replace('{avg_grade:.1f}', f'{avg_grade:.1f}')
    html_content = html_content.replace('{rows}', rows)
    
    return html_content.encode(ENCODING)

def create_http_response(status_code, body, content_type='text/html; charset=utf-8'):
    """Создает HTTP ответ с заданным статус-кодом и телом"""
    status_text = {
        200: "200 OK",
        303: "303 See Other",
        404: "404 Not Found",
        405: "405 Method Not Allowed"
    }.get(status_code, "500 Internal Server Error")
    
    headers = [
        f"HTTP/1.1 {status_text}",
        f"Server: {SERVER_NAME}",
        f"Content-Type: {content_type}",
        f"Content-Length: {len(body)}",
        f"Date: {datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')}",
        "Connection: close",
        "",
        ""
    ]
    return "\r\n".join(headers).encode(ENCODING) + body

def http_redirect(location):
    """Создает HTTP редирект"""
    headers = [
        "HTTP/1.1 303 See Other",
        f"Location: {location}",
        f"Server: {SERVER_NAME}",
        f"Date: {datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')}",
        "Connection: close",
        "",
        ""
    ]
    return "\r\n".join(headers).encode(ENCODING)

def handle_client(conn, addr):
    """Обрабатывает HTTP запрос от клиента"""
    with conn:
        try:
            req = conn.recv(8192).decode(ENCODING)
            if not req:
                return

            lines = req.splitlines()
            if not lines:
                return
                
            first_line = lines[0]
            parts = first_line.split()
            if len(parts) < 3:
                return
                
            method, path, version = parts
            headers_body = req.split("\r\n\r\n", 1)
            headers = headers_body[0]
            body = headers_body[1] if len(headers_body) > 1 else ""
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {addr} -> {method} {path}")

            if method == 'GET' and path == '/':
                with LOCK:
                    data = load_data()
                response = create_http_response(200, render_page(data))
                conn.sendall(response)

            elif method == 'POST' and path == '/add':
                content_type_line = next((line for line in headers.splitlines() if line.lower().startswith('content-type:')), "")
                
                if 'application/x-www-form-urlencoded' in content_type_line:
                    parsed = urllib.parse.parse_qs(body)
                    subject = urllib.parse.unquote(parsed.get('subject', [''])[0]).strip()
                    grade = urllib.parse.unquote(parsed.get('grade', [''])[0]).strip()
                    
                    # Валидация данных
                    if subject and grade and grade.isdigit() and 1 <= int(grade) <= 5:
                        with LOCK:
                            data = load_data()
                            data.append({"subject": subject, "grade": grade})
                            save_data(data)
                        print(f"Добавлена оценка: {subject} - {grade}")
                        conn.sendall(http_redirect('/'))
                    else:
                        error_html = "<html><body><h1>Ошибка валидации</h1><p>Проверьте правильность введенных данных.</p><a href='/'>Вернуться на главную</a></body></html>"
                        response = create_http_response(400, error_html.encode(ENCODING))
                        conn.sendall(response)
                else:
                    error_html = "<html><body><h1>Ошибка</h1><p>Неподдерживаемый Content-Type</p><a href='/'>Вернуться на главную</a></body></html>"
                    response = create_http_response(415, error_html.encode(ENCODING))
                    conn.sendall(response)
            else:
                error_html = """<!DOCTYPE html><html><head><title>404 Not Found</title></head><body><h1>404 Not Found</h1><p>Страница не найдена</p><p><a href="/">Вернуться на главную</a></p></body></html>"""
                response = create_http_response(404, error_html.encode(ENCODING))
                conn.sendall(response)
                
        except Exception as e:
            print(f"Ошибка обработки запроса от {addr}: {e}")

def main():
    print("HTTP Сервер")
    print("=" * 20)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        
        print(f"Сервер запущен на http://{HOST}:{PORT}/")
        print(f"Файл: template.html")
        print(f"Протокол: HTTP/1.1")
        print(f"Многопоточность: Включена")
        print("\nНажмите Ctrl+C для остановки...")
        
        try:
            while True:
                conn, addr = s.accept()
                thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
                thread.start()
        except KeyboardInterrupt:
            print("\nСервер остановлен")

if __name__ == '__main__':
    main()
```

### HTML Шаблон (task5/template.html)

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Система оценок</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .stats {
            display: flex;
            justify-content: space-around;
            margin: 2rem 0;
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 10px;
        }
        
        .stat {
            text-align: center;
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: #667eea;
        }
        
        .form-section {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 2rem 0;
        }
        
        .form-group {
            display: flex;
            gap: 1rem;
            align-items: end;
        }
        
        .form-field {
            flex: 1;
        }
        
        .form-field label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: bold;
        }
        
        .form-field input {
            width: 100%;
            padding: 0.5rem;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        
        .btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            cursor: pointer;
        }
        
        .btn:hover {
            background: #5a6fd8;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 2rem 0;
        }
        
        th, td {
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        
        th {
            background: #f8f9fa;
            font-weight: bold;
        }
        
        .footer {
            text-align: center;
            color: #666;
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid #eee;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Система оценок</h1>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-number">{total_grades}</div>
                <div>Всего оценок</div>
            </div>
            <div class="stat">
                <div class="stat-number">{avg_grade:.1f}</div>
                <div>Средний балл</div>
            </div>
        </div>
        
        <div class="form-section">
            <h3>Добавить новую оценку</h3>
            <form action="/add" method="post">
                <div class="form-group">
                    <div class="form-field">
                        <label for="subject">Дисциплина:</label>
                        <input type="text" id="subject" name="subject" required>
                    </div>
                    <div class="form-field">
                        <label for="grade">Оценка:</label>
                        <input type="number" id="grade" name="grade" min="1" max="5" required>
                    </div>
                    <button type="submit" class="btn">Добавить</button>
                </div>
            </form>
        </div>
        
        <h3>Список оценок</h3>
        <table>
            <thead>
                <tr>
                    <th>Дисциплина</th>
                    <th>Оценка</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
        
        <div class="footer">
            <p>Лабораторная работа №1 - Сетевые технологии | Губанов Егор, K3340</p>
        </div>
    </div>
</body>
</html>
```

## Запуск

1. Убедитесь, что файл `template.html` находится в той же папке, что и `server.py`
2. Запустите сервер:
   ```bash
   python task5/server.py
   ```
3. Откройте браузер и перейдите по адресу: http://127.0.0.1:8005

## Результат

**Сервер:**
```
HTTP Сервер
====================
Сервер запущен на http://127.0.0.1:8005/
Файл: template.html
Протокол: HTTP/1.1
Многопоточность: Включена

Нажмите Ctrl+C для остановки...
[14:30:15] ('127.0.0.1', 54321) -> GET /
[14:30:20] ('127.0.0.1', 54321) -> POST /add
Добавлена оценка: Математика - 5
[14:30:20] ('127.0.0.1', 54322) -> GET /
```

**Браузер:**
- Отображается веб-интерфейс для управления оценками
- Можно добавлять новые оценки через форму
- Оценки группируются по предметам в таблице
- Отображается статистика (общее количество и средний балл)

## Выводы

1. Реализован полнофункциональный веб-сервер с обработкой GET и POST запросов
2. Добавлена поддержка HTML форм и валидация данных
3. Реализовано сохранение данных в JSON файл
4. Добавлена группировка оценок по предметам
5. Использована многопоточность для обработки множественных запросов
6. Поддерживается кириллица в названиях предметов
7. Создан красивый и функциональный веб-интерфейс
