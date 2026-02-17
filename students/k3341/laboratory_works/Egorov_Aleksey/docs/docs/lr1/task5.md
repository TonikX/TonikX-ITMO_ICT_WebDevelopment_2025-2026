# Задание
Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.

**Требования:**

- Принять и записать информацию о дисциплине и оценке по дисциплине.
- Отдать информацию обо всех оценках по дисциплинам в виде HTML-страницы.
 
***

# Решение

## Сервер

```python
import socket
from urllib.parse import parse_qs

HOST = '127.0.0.1'
PORT = 9090

grades = []


def handle_request(request):
    lines = request.split('\r\n')
    if len(lines) < 1:
        return "HTTP/1.1 400 Bad Request\r\n\r\n"

    request_line = lines[0]
    try:
        method, path, _ = request_line.split()
    except ValueError:
        return "HTTP/1.1 400 Bad Request\r\n\r\n"

    if method == "GET":
        response_body = "<html><body><h2>Список оценок</h2><ul>"
        for grade in grades:
            response_body += f"<li>{grade['subject']}: {grade['mark']}</li>"
        response_body += "</ul>"
        response_body += '''
            <h3>Добавить новую оценку</h3>
            <form method="POST">
                Предмет: <input name="subject"><br>
                Оценка: <input name="mark"><br>
                <input type="submit" value="Добавить">
            </form>
        '''
        response_body += "</body></html>"

        response = (
            "HTTP/1.1 200 OK\r\n"
            f"Content-Length: {len(response_body.encode())}\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            "\r\n"
            + response_body
        )
        return response

    elif method == "POST":
        try:
            empty_line_index = lines.index('')
            body = '\r\n'.join(lines[empty_line_index + 1:])
        except ValueError:
            body = lines[-1]

        data = parse_qs(body)
        subject = data.get("subject", [""])[0]
        mark = data.get("mark", [""])[0]

        if subject and mark:
            grades.append({"subject": subject, "mark": mark})

        response = (
            "HTTP/1.1 303 See Other\r\n"
            "Location: /\r\n"
            "Content-Length: 0\r\n"
            "\r\n"
        )
        return response

    else:
        return "HTTP/1.1 405 Method Not Allowed\r\n\r\n"


def main():
    sock = socket.socket()
    sock.bind((HOST, PORT))
    sock.listen(1)

    print(f"Сервер запущен {HOST}:{PORT}")

    while True:
        conn, addr = sock.accept()
        print('Подключение:', addr)

        request = b""
        while True:
            part = conn.recv(1024)
            if not part:
                break
            request += part
            if len(part) < 1024:
                break
        request = request.decode()
        print("Полученный запрос:\n", request)

        response = handle_request(request)
        conn.sendall(response.encode())
        conn.close()

if __name__ == "__main__":
    main()

# http://localhost:9090/
```

Вспомогательные классы:

request.py
```python
from functools import lru_cache
from urllib.parse import parse_qs, urlparse


class Request:
    def __init__(self, method, target, version, headers, rfile):
        self.method = method
        self.target = target
        self.version = version
        self.headers = headers
        self.rfile = rfile

    @property
    def path(self):
        return self.url.path
    
    @property
    @lru_cache(maxsize=None)
    def query(self):
        return parse_qs(self.url.query)
    
    @property
    @lru_cache(maxsize=None)
    def url(self):
        return urlparse(self.target)
    

    @property
    def body(self):
        try:
            size = self.headers.get('Content-Length')
            if not size:
                return {}
        
            content_length = int(size)
            if content_length == 0:
                return {}
            
            raw_body = self.rfile.read(content_length)
            if not raw_body:
                return {}
            
            body_str = raw_body.decode('utf-8')
            return parse_qs(body_str)
        
        except (ValueError, UnicodeDecodeError, Exception) as e:
            print(f"Error parsing request body: {e}")
        return {}
```
***

# Пояснение

# Веб-сервер для хранения оценок на Python

Этот код реализует простой HTTP-сервер, который позволяет просматривать и добавлять оценки через веб-интерфейс.

## Принцип работы

1. Сервер запускается и слушает локальный порт 9090
2. При переходе в браузере на `http://localhost:9090` открывается страница со списком оценок
3. Через форму можно добавить новую оценку (предмет и оценку)
4. Все данные хранятся в оперативной памяти (список `grades`)

## Как это работает

### GET-запрос
- Сервер отдаёт HTML-страницу со списком всех сохранённых оценок
- Внизу страницы находится форма для добавления новой оценки

### POST-запрос
- Когда пользователь отправляет форму, сервер получает данные
- Извлекает предмет (`subject`) и оценку (`mark`)
- Добавляет их в список `grades`
- Перенаправляет обратно на главную страницу (код 303)

## Основные функции

- **`handle_request(request)`** — разбирает HTTP-запрос и формирует ответ
- **`main()`** — главный цикл сервера, принимает подключения

## Особенности реализации

- Сервер обрабатывает только GET и POST методы
- Данные формы разбираются через `urllib.parse.parse_qs`
- При добавлении оценки происходит редирект (чтобы избежать повторной отправки при обновлении)
- Все ответы возвращаются в кодировке UTF-8
- Сервер обрабатывает одно подключение за раз (без многопоточности)

## Формат хранения

Оценки хранятся как список словарей:
```python
grades = [
    {"subject": "Математика", "mark": "5"},
    {"subject": "Физика", "mark": "4"}
]