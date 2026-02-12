## Задание 5:
Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.

### Используемые технологии:
- Python `socket`
- HTTP/1.1
- Протокол TCP

### Файлы:


**server.py**
```python
import socket
from urllib.parse import urlparse, parse_qs
from email.utils import formatdate

GRADES: dict[str, list[str]] = {}

HOST = "127.0.0.1"
PORT = 8080
SERVER_NAME = "GradesServer"


class MyHTTPServer:
    def __init__(self, host: str, port: int, name: str):
        self.host = host
        self.port = port
        self.name = name

    # Запуск сервера на сокете, обработка входящих соединений
    def serve_forever(self):
        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serv_sock.bind((self.host, self.port))
        serv_sock.listen(10)
        print(f"{self.name} listening at http://{self.host}:{self.port}/")

        try:
            while True:
                conn, addr = serv_sock.accept()
                try:
                    self.serve_client(conn)
                except Exception as e:
                    self.send_error(conn, e)
                finally:
                    conn.close()
        finally:
            serv_sock.close()

    # Обработка клиентского подключения
    def serve_client(self, conn: socket.socket):
        request_line, headers, body = self.parse_request(conn)
        response = self.handle_request(request_line, headers, body)
        self.send_response(conn, response)

    # Обработка request line и подготовка rfile
    def parse_request(self, conn: socket.socket):
        rfile = conn.makefile("rb")
        line = rfile.readline(64 * 1024)
        if not line:
            raise Exception("Empty request")
        try:
            line_str = line.decode("iso-8859-1").strip()
        except UnicodeDecodeError:
            raise Exception("Cannot decode request line")
        parts = line_str.split()
        if len(parts) != 3:
            raise Exception("Malformed request line")
        method, target, version = parts
        if version != "HTTP/1.1":
            raise Exception("Unsupported HTTP version")
        headers = self.parse_headers(rfile)
        body = None
        if "content-length" in headers:
            length = int(headers["content-length"])
            body = rfile.read(length)
        return (method, target, version), headers, body

    # Обработка headers
    def parse_headers(self, rfile):
        headers = {}
        for _ in range(100):
            line = rfile.readline(64 * 1024)
            if line in (b"\r\n", b"\n", b""):
                break
            try:
                line_str = line.decode("iso-8859-1").strip()
            except UnicodeDecodeError:
                continue
            if ":" in line_str:
                key, value = line_str.split(":", 1)
                headers[key.lower().strip()] = value.strip()
        return headers

    # Обработка GET/POST
    def handle_request(self, request_line, headers, body):
        method, target, version = request_line
        parsed_url = urlparse(target)
        path = parsed_url.path
        query = parse_qs(parsed_url.query, keep_blank_values=True)

        if method == "GET" and path == "/":
            html = self.render_index_html()
            return 200, "OK", {"Content-Type": "text/html; charset=utf-8"}, html.encode("utf-8")

        if method == "POST" and path == "/submit":
            post_data = {}
            if body:
                post_data = parse_qs(body.decode("utf-8"), keep_blank_values=True)
            for k, v in query.items():
                post_data.setdefault(k, []).extend(v)

            subject = post_data.get("subject", [""])[0].strip()
            grade = post_data.get("grade", [""])[0].strip()
            if not subject or not grade:
                return 400, "Bad Request", {"Content-Type": "text/plain"}, b"Missing subject or grade"

            GRADES.setdefault(subject, []).append(grade)

            # redirect after POST
            return 303, "See Other", {"Location": "/"}, b""

        return 404, "Not Found", {"Content-Type": "text/plain"}, b"Not Found"

    # Отправка ответа
    def send_response(self, conn: socket.socket, response):
        status, reason, headers, body = response
        wfile = conn.makefile("wb")
        wfile.write(f"HTTP/1.1 {status} {reason}\r\n".encode("iso-8859-1"))
        headers["Date"] = formatdate(usegmt=True)
        headers["Server"] = self.name
        headers["Content-Length"] = str(len(body))
        headers["Connection"] = "close"
        for k, v in headers.items():
            wfile.write(f"{k}: {v}\r\n".encode("iso-8859-1"))
        wfile.write(b"\r\n")
        wfile.write(body)
        wfile.flush()

    def send_error(self, conn: socket.socket, error: Exception):
        body = str(error).encode("utf-8")
        self.send_response(conn, (500, "Internal Server Error", {"Content-Type": "text/plain"}, body))

    def render_index_html(self) -> str:
        if not GRADES:
            rows = "<tr><td colspan='2'>No records yet</td></tr>"
        else:
            rows = "\n".join(
                f"<tr><td>{self.escape(subject)}</td><td>{', '.join(self.escape(g) for g in grades)}</td></tr>"
                for subject, grades in GRADES.items()
            )
        return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Grades</title>
</head>
<body>
<h1>Grades</h1>
<table border="1">
<tr><th>Subject</th><th>Grades</th></tr>
{rows}
</table>
<form method="POST" action="/submit">
<label>Subject: <input name="subject" required></label>
<label>Grade: <input name="grade" required></label>
<button type="submit">Save</button>
</form>
</body>
</html>"""

    @staticmethod
    def escape(text: str) -> str:
        return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&#39;"))


if __name__ == "__main__":
    server = MyHTTPServer(HOST, PORT, SERVER_NAME)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")

```

### Результат работы:
Сервер:
```
GradesServer listening at http://127.0.0.1:8080/
```
Клиент:
1. При GET-запросе отображается HTML-страница с таблицей оценок и формой добавления новой записи.

2. При POST-запросе данные формы добавляются на сервер, и страница автоматически обновляется (редирект на /).
