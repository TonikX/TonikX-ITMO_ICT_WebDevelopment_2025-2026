# Задание 5: Веб-сервер для обработки GET и POST запросов

## Цель работы
Реализовать простой веб-сервер, обрабатывающий GET и POST HTTP-запросы для добавления и отображения оценок по дисциплинам.

## Код программы

### server.py
```python
import socket
from urllib.parse import unquote, parse_qs

HOST = "127.0.0.1"
PORT = 8080

grades = []

def build_html():
    html = "<html><head><title>Оценки</title></head><body>"
    html += "<h1>Оценки по дисциплинам</h1>"
    html += """
    <form method="POST" action="/">
        Дисциплина: <input type="text" name="discipline" required>
        Оценка: <input type="text" name="grade" required>
        <input type="submit" value="Добавить">
    </form>
    <hr>
    """
    if grades:
        html += "<ul>"
        for g in grades:
            html += f"<li>{g['discipline']}: {g['grade']}</li>"
        html += "</ul>"
    else:
        html += "<p>Нет данных.</p>"
    html += "</body></html>"
    return html

def handle_request(request_text):
    lines = request_text.split("\r\n")
    request_line = lines[0]
    method, path, _ = request_line.split()
    body = "\r\n".join(lines[lines.index("")+1:])

    if method == "POST":
        params = parse_qs(body)
        discipline = unquote(params.get("discipline", [""])[0])
        grade = unquote(params.get("grade", [""])[0])
        if discipline and grade:
            grades.append({"discipline": discipline, "grade": grade})
    html = build_html()
    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: {len(html.encode('utf-8'))}\r\n\r\n{html}"
    return response

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen(5)
        print(f"Сервер запущен на http://{HOST}:{PORT}")
        while True:
            conn, addr = srv.accept()
            with conn:
                data = conn.recv(4096).decode("utf-8")
                if not data:
                    continue
                print(f"Запрос от {addr}:\n{data.splitlines()[0]}")
                response = handle_request(data)
                conn.sendall(response.encode("utf-8"))

if __name__ == "__main__":
    main()
```

## Описание работы программы

### Функциональность сервера
- **Обработка GET запросов**: Отображает HTML-страницу с формой и списком оценок
- **Обработка POST запросов**: Принимает данные из формы и добавляет их в список оценок
- **Хранение данных**: Оценки хранятся в памяти в списке grades