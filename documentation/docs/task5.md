# Задание 5

Написать простой **веб-сервер** для обработки **GET** и **POST** HTTP-запросов с помощью `socket` в Python.

**Требования:**
- Сервер должен:
  - Принять и записать информацию о дисциплине и оценке (в памяти процесса).
  - Отдать информацию обо всех оценках по дисциплинам в виде HTML-страницы (одна строка на дисциплину со списком оценок).
- Протокол: TCP (HTTP поверх TCP).

---

## Решение

### Сервер
```python
import socket
from urllib.parse import parse_qs

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8083

# Память сервера: "дисциплина" -> список оценок
grades_by_discipline = {}  # например: {"Математика": ["5", "4"]}

def build_html_page():
    table_rows = []
    if grades_by_discipline:
        for discipline, grades_list in grades_by_discipline.items():
            grades_text = ", ".join(grades_list) if grades_list else "—"
            table_rows.append(f"<tr><td>{discipline}</td><td>{grades_text}</td></tr>")
    else:
        table_rows.append("<tr><td colspan='2'>Нет данных</td></tr>")

    html = """<!DOCTYPE html>
<html lang="ru">
<meta charset="UTF-8">
<title>Журнал оценок</title>
<h1>Журнал оценок</h1>

<form action="/add" method="POST">
  <div>
    <label>Дисциплина: <input type="text" name="discipline"></label>
  </div>
  <div>
    <label>Оценка: <input type="text" name="grade"></label>
  </div>
  <div>
    <button type="submit">Добавить</button>
  </div>
</form>

<table border="1" cellpadding="6" cellspacing="0">
  <thead>
    <tr><th>Дисциплина</th><th>Оценки</th></tr>
  </thead>
  <tbody>
    {rows}
  </tbody>
</table>
""".format(rows=''.join(table_rows))
    return html

def read_http_request(client_socket):
    data = b""
    while b"\r\n\r\n" not in data:
        chunk = client_socket.recv(4096)
        if not chunk:
            break
        data += chunk

    header_part, _, body_rest = data.partition(b"\r\n\r\n")
    header_text = header_part.decode("iso-8859-1", errors="ignore")
    lines = header_text.split("\r\n")
    request_line = lines[0] if lines else ""
    try:
        method, path, version = request_line.split(" ")
    except ValueError:
        method, path, version = "", "", ""

    headers = {}
    for line in lines[1:]:
        if ":" in line:
            k, v = line.split(":", 1)
            headers[k.strip().lower()] = v.strip()

    content_length = int(headers.get("content-length", "0") or "0")
    body = body_rest
    while len(body) < content_length:
        chunk = client_socket.recv(4096)
        if not chunk:
            break
        body += chunk

    return method, path, version, headers, body

def build_http_response(status_code, body_text, content_type="text/html; charset=UTF-8"):
    if status_code == 200:
        status_line = "HTTP/1.1 200 OK"
    elif status_code == 404:
        status_line = "HTTP/1.1 404 Not Found"
    else:
        status_line = f"HTTP/1.1 {status_code}"

    body_bytes = body_text.encode("utf-8")
    headers_lines = [
        status_line,
        f"Content-Type: {content_type}",
        f"Content-Length: {len(body_bytes)}",
        "Connection: close",
    ]
    return ("\r\n".join(headers_lines) + "\r\n\r\n").encode("utf-8") + body_bytes

def handle_client(client_socket):
    try:
        method, path, version, headers, body = read_http_request(client_socket)

        if method == "GET" and path.startswith("/"):
            page = build_html_page()
            client_socket.sendall(build_http_response(200, page))
            return

        if method == "POST" and path == "/add":
            form_text = body.decode("utf-8", errors="ignore")
            form_data = parse_qs(form_text)
            discipline = (form_data.get("discipline", [""])[0] or "").strip()
            grade = (form_data.get("grade", [""])[0] or "").strip()

            if discipline and grade:
                grades_by_discipline.setdefault(discipline, []).append(grade)

            page = build_html_page()
            client_socket.sendall(build_http_response(200, page))
            return

        not_found = "<!doctype html><meta charset='utf-8'><h1>404 Not Found</h1>"
        client_socket.sendall(build_http_response(404, not_found))
    finally:
        try:
            client_socket.close()
        except Exception:
            pass

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"Журнал-HTTP-сервер запущен на http://{SERVER_HOST}:{SERVER_PORT}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            handle_client(client_socket)
    except KeyboardInterrupt:
        print("\nСервер остановлен пользователем.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
```

---

## Подробное пояснение

### 1) Общая идея
- Мы пишем **микро-HTTP-сервер** на чистых сокетах: читаем текст запроса, парсим стартовую строку, заголовки, при необходимости тело.
- Поддерживаем **два маршрута**:
  - `GET /` — отдать HTML-страницу с формой и таблицей оценок.
  - `POST /add` — принять поля `discipline` и `grade`, добавить их в память, вернуть обновлённую HTML-страницу.

### 2) Как читается HTTP-запрос
- TCP — поток байт. Мы читаем из сокета порциями, пока не встретим **разделитель заголовков и тела**: `\r\n\r\n`.
- Первая строка (Request-Line) вида: `GET / HTTP/1.1` → разбиваем на `method`, `path`, `version`.
- Заголовки кладём в словарь `headers` с ключами в нижнем регистре (удобнее искать).
- Если есть `Content-Length: N`, дочитываем ещё `N` байт для **тела** запроса.

### 3) Как парсим данные формы (POST)
- Браузер по умолчанию шлёт `<form method="POST">` в формате `application/x-www-form-urlencoded`, например:
  ```
  discipline=%D0%9C%D0%B0%D1%82%D0%B5%D0%BC%D0%B0%D1%82%D0%B8%D0%BA%D0%B0&grade=5
  ```
- Декодируем тело как UTF-8 и пропускаем через `parse_qs`, получая словарь списков:
  ```python
  {"discipline": ["Математика"], "grade": ["5"]}
  ```
- Берём **первый элемент** каждого списка, подрезаем пробелы `.strip()`.  
  Если поле отсутствует/пустое — просто ничего не добавляем.

### 4) Хранилище данных
- `grades_by_discipline: dict[str, list[str]]` — словарь в памяти процесса.
- При добавлении:
  ```python
  grades_by_discipline.setdefault(discipline, []).append(grade)
  ```
  Это создаёт пустой список для новой дисциплины и добавляет оценку.

### 5) Формирование HTML-страницы
- В `build_html_page()` строим таблицу: **одна строка = одна дисциплина**, справа — список всех её оценок, объединённый через запятую.
- Если данных нет — выводим одну строку «Нет данных».
- Выдаём минимальный, «учебный» HTML (без лишнего оформления).

### 6) Формирование HTTP-ответа
- Собираем ответ вручную:
  - Статус `HTTP/1.1 200 OK` (или 404).
  - Заголовки: `Content-Type`, `Content-Length` (**в байтах**), `Connection: close`.
  - Пустая строка `\r\n\r\n`.
  - Тело (HTML).
- Почему `Content-Length` в байтах: HTTP — байтовый протокол; UTF-8 символ может занимать больше 1 байта.

### 7) Жизненный цикл запросов
1. Браузер делает `GET /` → сервер возвращает страницу с формой и текущей таблицей.
2. Пользователь отправляет форму → браузер шлёт `POST /add` с телом.
3. Сервер парсит тело, добавляет запись, снова возвращает **HTML-страницу** (без редиректа — проще).

### 8) Почему закрываем соединение
- Заголовок `Connection: close` — после ответа закрываем сокет. Так проще: «один запрос — один ответ».
- Браузер сам создаст новое соединение при следующем запросе.

---

## Как запустить и проверить
1. Запустить сервер:
   ```bash
   python grades_server.py
   ```
2. Открыть в браузере: `http://127.0.0.1:8083/`
3. Заполнить форму: дисциплина и оценка → **Добавить**.  
   На странице появится строка с дисциплиной и список её оценок.
4. Добавить ту же дисциплину ещё раз — увидите накопление оценок в одной строке.

---
