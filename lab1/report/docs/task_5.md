### Задание 5 (Мини веб-сервер: GET/POST)
Сервер:
```bash
import socket
import urllib.parse
import json
import os


HOST = "localhost"
PORT = 8089
DATA_FILE = "grades.json"


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except Exception:
                return {}
    return {}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def build_html(grades):
    rows = "".join(f"<tr><td>{subj}</td><td>{grade}</td></tr>" for subj, grade in grades.items())
    return f"""<!doctype html>
<html lang="ru">
<head><meta charset="utf-8"><title>Оценки</title></head>
<body>
  <h1>Оценки по дисциплинам</h1>
  <form method="POST" action="/add">
    <label>Дисциплина: <input name="subject" required></label>
    <label>Оценка: <input name="grade" required></label>
    <button type="submit">Сохранить</button>
  </form>
  <h2>Все оценки</h2>
  <table border="1" cellspacing="0" cellpadding="6">
    <tr><th>Дисциплина</th><th>Оценка</th></tr>
    {rows}
  </table>
</body>
</html>"""


def http_response(status, body, content_type="text/html; charset=utf-8", extra_headers=None):
    if isinstance(body, str):
        body_bytes = body.encode("utf-8")
    else:
        body_bytes = body
    headers = [
        f"HTTP/1.1 {status}",
        "Server: GradesServer",
        f"Content-Length: {len(body_bytes)}",
        f"Content-Type: {content_type}",
        "Connection: close",
    ]
    if extra_headers:
        headers.extend(extra_headers)
    headers.append("")
    headers.append("")
    return ("\r\n".join(headers)).encode("utf-8") + body_bytes


def parse_request(raw):
    try:
        header_part, body = raw.split(b"\r\n\r\n", 1)
    except ValueError:
        header_part, body = raw, b""
    lines = header_part.split(b"\r\n")
    request_line = lines[0].decode("utf-8", errors="replace")
    method, path, _ = request_line.split(" ")
    headers = {}
    for line in lines[1:]:
        if b":" in line:
            k, v = line.split(b":", 1)
            headers[k.decode().strip().lower()] = v.decode().strip()
    return method, path, headers, body


def main():
    grades = load_data()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"[GRADES SERVER] http://{HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            with conn:
                raw = conn.recv(65536)
                if not raw:
                    continue
                method, path, headers, body = parse_request(raw)
                if method == "GET" and path == "/":
                    html = build_html(grades)
                    conn.sendall(http_response("200 OK", html))
                elif method == "POST" and path == "/add":
                    ctype = headers.get("content-type", "")
                    if "application/x-www-form-urlencoded" in ctype:
                        params = urllib.parse.parse_qs(body.decode("utf-8", errors="replace"))
                        subj = (params.get("subject") or [""])[0].strip()
                        grade = (params.get("grade") or [""])[0].strip()
                        if subj:
                            grades[subj] = grade
                            save_data(grades)
                        # redirect back to /
                        conn.sendall(http_response("303 See Other", b"", extra_headers=[ "Location: /" ]))
                    else:
                        conn.sendall(http_response("415 Unsupported Media Type", "<h1>Use application/x-www-form-urlencoded</h1>"))
                else:
                    conn.sendall(http_response("404 Not Found", "<h1>404</h1>"))


if __name__ == "__main__":
    main()
```

```bash
python task5_web_server/grades_server.py
```
Откройте `http://localhost:8089/`, добавляйте записи через форму. Данные сохраняются в `grades.json`.
