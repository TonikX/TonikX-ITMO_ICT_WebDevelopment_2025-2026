import socket
from urllib.parse import parse_qs

HOST = "127.0.0.1"
PORT = 8081
ENC = "utf-8"

GRADES = {}

def http_response(status: str, body: str, content_type: str = "text/html; charset=UTF-8") -> bytes:
    b = body.encode(ENC)
    head = (
            status + "\r\n"
                     f"Content-Type: {content_type}\r\n"
                     f"Content-Length: {len(b)}\r\n"
                     "Connection: close\r\n"
                     "\r\n"
    )
    return head.encode(ENC) + b

# Генерация HTML-страницы со списком предметов и оценок.
def render_index() -> str:
    rows = []
    for subj in sorted(GRADES.keys(), key=str.lower):  # сортируем предметы по алфавиту
        grades = ", ".join(str(x) for x in GRADES[subj]) or "—"
        rows.append(f"<tr><td>{escape(subj)}</td><td>{grades}</td></tr>")
    # Если нет данных — пишем одну строку с сообщением
    table = "\n".join(rows) if rows else '<tr><td colspan="2">Пока нет данных</td></tr>'
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Журнал</title></head>
<body>
<h1>Журнал оценок</h1>
<p>Добавляйте записи POST-запросом на <code>/add.</p>
<table border="1" cellpadding="4" cellspacing="0">
  <tr><th>Дисциплина</th><th>Оценки</th></tr>
  {table}
</table>
<p><a href="/form">Добавить оценку</a></p>
</body></html>"""

# HTML-форма для добавления оценки
def render_form() -> str:
    return """<!doctype html>
<html lang="ru">
<head><meta charset="utf-8"><title>Добавить оценку</title></head>
<body>
<h1>Добавить оценку</h1>
<form action="/add" method="post">
  <label>Дисциплина: <input type="text" name="subject"></label><br><br>
  <label>Оценка: <input type="number" name="grade" min="1" max="5"></label><br><br>
  <button type="submit">Отправить</button>
</form>
<p><a href="/">Вернуться в журнал</a></p>
</body></html>"""

def escape(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;").replace("'", "&#39;"))

# Чтение HTTP-запроса из сокета.
def parse_request(conn):
    data = b""
    while b"\r\n\r\n" not in data:
        chunk = conn.recv(4096)
        if not chunk:
            break
        data += chunk
        if len(data) > 1_000_000:
            break
    header, _, body = data.partition(b"\r\n\r\n")
    lines = header.decode(ENC, errors="replace").split("\r\n")
    request_line = lines[0] if lines else ""
    parts = request_line.split()
    method = parts[0] if len(parts) > 0 else ""
    path = parts[1] if len(parts) > 1 else "/"
    # Словарь заголовков
    headers = {}
    for line in lines[1:]:
        if ":" in line:
            k, v = line.split(":", 1)
            headers[k.strip().lower()] = v.strip()
    # Определяем длину тела
    try:
        clen = int(headers.get("content-length", "0"))
    except ValueError:
        clen = 0
    while len(body) < clen:
        chunk = conn.recv(clen - len(body))
        if not chunk:
            break
        body += chunk
    return method, path, headers, body

# Обработка GET-запроса
def handle_get(conn, path):
    if path in ("/", "/index.html"):
        html = render_index()
        conn.sendall(http_response("HTTP/1.1 200 OK", html))
    elif path == "/form":
        html = render_form()
        conn.sendall(http_response("HTTP/1.1 200 OK", html))
    else:
        conn.sendall(http_response("HTTP/1.1 404 Not Found", "Not Found", "text/plain; charset=UTF-8"))

# Обработка POST-запроса на добавление оценки.
def handle_post_add(conn, headers, body):
    form = parse_qs(body.decode(ENC, errors="replace"))
    subject = (form.get("subject", [""])[0] or "").strip()
    grade_raw = (form.get("grade", [""])[0] or "").strip()
    if not subject or not grade_raw:
        conn.sendall(http_response("HTTP/1.1 400 Bad Request", "subject и grade обязательны", "text/plain; charset=UTF-8"))
        return
    try:
        grade = int(grade_raw)
    except ValueError:
        conn.sendall(http_response("HTTP/1.1 400 Bad Request", "grade должен быть целым числом", "text/plain; charset=UTF-8"))
        return
    GRADES.setdefault(subject, []).append(grade)
    resp = (
        "HTTP/1.1 303 See Other\r\n"
        "Location: /\r\n"
        "Connection: close\r\n"
        "Content-Length: 0\r\n"
        "\r\n"
    )
    conn.sendall(resp.encode(ENC))

def main():
    print(f"Сервер журнала: http://{HOST}:{PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen(10)
        while True:
            conn, addr = srv.accept()
            try:
                method, path, headers, body = parse_request(conn)
                if method == "GET":
                    handle_get(conn, path)
                elif method == "POST" and path == "/add":
                    handle_post_add(conn, headers, body)
                else:
                    conn.sendall(http_response("HTTP/1.1 404 Not Found", "Not Found", "text/plain; charset=UTF-8"))
            except Exception as e:
                conn.sendall(http_response("HTTP/1.1 500 Internal Server Error", f"Error: {e}", "text/plain; charset=UTF-8"))
            finally:
                try:
                    conn.shutdown(socket.SHUT_RDWR)
                except OSError:
                    pass
                conn.close()

if __name__ == "__main__":
    main()
