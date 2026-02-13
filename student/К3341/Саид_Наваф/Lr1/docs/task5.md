# Задание 5 - HTTP сервер с формами

## Описание задания

Реализовать HTTP‑сервер на Python, который обрабатывает GET и POST запросы, работает с HTML‑формами и сохраняет оценки по предметам в JSON‑файл. Сервер должен поддерживать как JSON‑API, так и обычную HTML‑форму для ввода данных.

## Теоретические основы

### HTTP запросы и ответы

HTTP‑сервер принимает стартовую строку запроса, заголовки и, при необходимости, тело сообщения.  
В данном задании используются методы:

- **GET** — получение страницы (форма, список оценок).
- **POST** — отправка данных (оценки) на сервер для сохранения.

Сервер должен корректно разбирать метод, путь, версию протокола, заголовки и содержимое тела.

### HTML формы и кодировка

HTML‑форма отправляет данные в формате `application/x-www-form-urlencoded`.  
Тело POST‑запроса содержит пары `ключ=значение`, разделённые `&`, с заменой пробелов на `+` и кодированием специальных символов.

Серверу необходимо:

- Прочитать `Content-Length` и дочитать указанное количество байт тела.
- Распарсить строки вида `lesson=Math&grade=95`.
- Выполнить базовую декодировку (`+` → пробел).

## Структура проекта

```text
task5/
├── webserver.py   # HTTP сервер
├── request.py     # Модели HTTP-запроса и ответа
└── lesson.py      # Логика работы с оценками и HTML
```

## Реализация

### Модели Request и Response (request.py)

```python
from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class Request:
    method: str
    url: str
    http_version: str
    params: Dict[str, str]
    headers: Dict[str, str]
    content: Optional[str]

@dataclass
class Response:
    status: int
    reason: str
    http_version: str = "HTTP/1.1"
    headers: Dict[str, str] = None
    body: str = ""
```

**Назначение:**

- `Request` хранит разобранный HTTP‑запрос (метод, путь, параметры, заголовки, тело).
- `Response` описывает HTTP‑ответ (код, текст причины, заголовки и тело).

### Логика оценок и HTML (lesson.py)

```python
import json
from typing import Dict
from request import Request, Response

class Lessons:
    def __init__(self, persist_file: str = None):
        self.lessons: Dict[str, int] = {}
        self.persist_file = persist_file
        if self.persist_file:
            try:
                with open(self.persist_file, "r") as f:
                    self.lessons = json.load(f)
            except Exception:
                self.lessons = {}

    def set_grade(self, lesson: str, grade: int):
        self.lessons[lesson] = grade
        if self.persist_file:
            with open(self.persist_file, "w") as f:
                json.dump(self.lessons, f)

    def get_grades_html(self) -> str:
        if not self.lessons:
            return "<h1>No grades yet</h1>"
        out = "<ul>"
        for k, v in self.lessons.items():
            out += f"<li>{k}: {v}</li>"
        out += "</ul>"
        return out
```

**Функции обработки запросов:**

```python
def parse_set_grades_req(lessons: Lessons, req: Request) -> Response:
    if not req.content:
        return Response(400, "Bad Request", body="empty content")
    try:
        j = json.loads(req.content)
        lessons.set_grade(j["lesson"], int(j["grade"]))
        return Response(200, "OK", body="OK")
    except Exception as e:
        return Response(400, "Bad Request", body=f"invalid json: {e}")

def parse_get_grades_req(lessons: Lessons, req: Request) -> Response:
    return Response(200, "OK", body=lessons.get_grades_html())
```

**HTML‑форма и её обработка:**

```python
def get_add_grade_form_html() -> str:
    return """
<html>
    <head>
        <meta charset="utf-8">
        <title>Add Lesson Grade</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="p-4">
        <div class="container">
            <h1 class="mb-3">Add Lesson and Grade</h1>
            <form method="post" action="/add" class="row g-3">
                <div class="col-md-8">
                    <label class="form-label">Lesson</label>
                    <input name="lesson" class="form-control" required />
                </div>
                <div class="col-md-4">
                    <label class="form-label">Grade</label>
                    <input name="grade" type="number" min="0" max="100" class="form-control" required />
                </div>
                <div class="col-12">
                    <button class="btn btn-primary">Submit</button>
                    <a href="/grades" class="btn btn-secondary ms-2">View Grades</a>
                </div>
            </form>
        </div>
    </body>
</html>
"""

def parse_set_grades_form(lessons: Lessons, req: Request) -> Response:
    # Expecting form-encoded body like: lesson=Math&grade=95
    if not req.content:
        return Response(400, "Bad Request", body="empty content")
    try:
        pairs = {}
        for part in req.content.split("&"):
            if "=" in part:
                k, v = part.split("=", 1)
                # Basic URL decode for + and %20
                k = k.replace("+", " ")
                v = v.replace("+", " ")
                pairs[k] = v
        lesson = pairs.get("lesson")
        grade = pairs.get("grade")
        if lesson is None or grade is None:
            return Response(400, "Bad Request", body="missing fields")
        lessons.set_grade(lesson, int(grade))
        # Redirect back to form or grades page
        return Response(303, "See Other", headers={"Location": "/grades"}, body="")
    except Exception as e:
        return Response(400, "Bad Request", body=f"invalid form data: {e}")
```

### HTTP‑сервер (webserver.py)

```python
import socket
import json
from request import Request, Response
from lesson import Lessons, parse_get_grades_req, parse_set_grades_req, get_add_grade_form_html, parse_set_grades_form

HOST = "127.0.0.1"
PORT = 8081

class MyHTTPServer:
    def __init__(self, host, port, persist=None):  # Fixed: __init__ instead of init
        self.host = host
        self.port = port
        self.lessons = Lessons(persist)

    def serve_forever(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv:
            serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            serv.bind((self.host, self.port))
            serv.listen(5)
            print(f"HTTP server on http://{self.host}:{self.port}")
            while True:
                conn, _ = serv.accept()
                try:
                    self.serve_client(conn)
                except Exception as e:
                    print("Error handling client:", e)
                finally:
                    conn.close()

    def recv_line(self, conn):
        line = b""
        while not line.endswith(b"\r\n"):
            part = conn.recv(1)
            if not part:
                break
            line += part
        return line.decode()

    def parse_headers(self, conn):
        headers = {}
        while True:
            line = self.recv_line(conn)
            if not line or line == "\r\n":
                break
            name, value = line.split(":", 1)
            headers[name.strip().lower()] = value.strip()
        return headers

    def parse_request(self, conn) -> Request:
        # First line
        first_line = self.recv_line(conn)
        if not first_line:
            raise ConnectionError("No request line")
        method, url, version = first_line.strip().split(" ", 2)  # Fixed: use 2 instead of 3-1
        headers = self.parse_headers(conn)
        body = None
        if "content-length" in headers:
            length = int(headers["content-length"])
            body = conn.recv(length).decode()
        params = {}
        if "?" in url:
            path, query = url.split("?", 1)
            url = path
            for q in query.split("&"):
                if "=" in q:
                    k, v = q.split("=", 1)
                    params[k] = v
        return Request(method, url, version, params, headers, body)

    def send_response(self, conn, resp: Response):
        headers = resp.headers or {}
        if "Content-Length" not in headers:
            headers["Content-Length"] = str(len(resp.body.encode()))
        if "Content-Type" not in headers:
            headers["Content-Type"] = "text/html; charset=utf-8"
        header_lines = "".join(f"{k}: {v}\r\n" for k, v in headers.items())
        status_line = f"{resp.http_version} {resp.status} {resp.reason}\r\n"
        out = (status_line + header_lines + "\r\n" + resp.body).encode()
        conn.sendall(out)

    def handle_request(self, req: Request) -> Response:
        # Serve HTML form at root
        if req.method == "GET" and req.url == "/":
            return Response(200, "OK", body=get_add_grade_form_html())
        # View grades
        if req.method == "GET" and req.url == "/grades":
            return parse_get_grades_req(self.lessons, req)
        # Accept JSON POST to /grades (API)
        if req.method == "POST" and req.url == "/grades":
            return parse_set_grades_req(self.lessons, req)
        # Accept form POST from HTML form
        if req.method == "POST" and req.url == "/add":
            return parse_set_grades_form(self.lessons, req)
        return Response(404, "Not Found", body="Not Found")

    def serve_client(self, conn):
        req = self.parse_request(conn)
        resp = self.handle_request(req)
        self.send_response(conn, resp)

if __name__ == "__main__":
    s = MyHTTPServer(HOST, PORT, persist="grades.json")
    s.serve_forever()
```

**Ключевые компоненты:**

1. **Разбор HTTP‑запроса**
   - Чтение стартовой строки (`method url version`).
   - Чтение и парсинг заголовков.
   - Чтение тела по `Content-Length`.
   - Разбор query‑параметров (`?a=1&b=2`).

2. **Маршрутизация (handle_request)**
   - `GET /` → HTML‑форма добавления оценки.
   - `GET /grades` → HTML‑список оценок.
   - `POST /grades` → приём JSON и сохранение оценки.
   - `POST /add` → приём данных формы и редирект на `/grades`.

3. **Формирование ответа**
   - Установка `Content-Length` и `Content-Type`, если не заданы.
   - Формирование статусной строки `HTTP/1.1 de> <reason>`.
   - Отправка заголовков и тела клиенту.

## Запуск приложения

### Шаг 1: Запуск сервера

```bash
cd task5
python webserver.py
```

Ожидаемый вывод:

```text
HTTP server on http://127.0.0.1:8081
```

### Шаг 2: Работа через браузер

1. Открыть `http://127.0.0.1:8081/` — форма добавления оценки.
2. Заполнить поля **Lesson** и **Grade**, отправить форму.
3. После редиректа открыть/увидеть `http://127.0.0.1:8081/grades` — список всех сохранённых оценок.

### Шаг 3: Проверка JSON‑API

Отправка оценки через `curl`:

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"lesson": "Math", "grade": 95}' \
     http://127.0.0.1:8081/grades
```

После этого страница `/grades` должна отобразить предмет и оценку, сохранённые в `grades.json`.
