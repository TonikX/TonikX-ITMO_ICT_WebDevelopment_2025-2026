import socket
import urllib.parse
from typing import Tuple, Dict
import data_store

HOST = "127.0.0.1"
PORT = 9095


def build_response(status: str, headers: Dict[str, str], body: str = "") -> bytes:
    """Формируем HTTP-ответ."""
    body_bytes = body.encode("utf-8")
    headers = {
        "Content-Type": "text/html; charset=utf-8",
        "Connection": "close",
        "Content-Length": str(len(body_bytes)),
        **headers,
    }
    lines = [f"HTTP/1.1 {status}"] + [f"{k}: {v}" for k, v in headers.items()]
    head = "\r\n".join(lines) + "\r\n\r\n"
    return head.encode("utf-8") + body_bytes


def parse_request(data: bytes) -> Tuple[str, str, Dict[str, str], bytes]:
    try:
        head, body = data.split(b"\r\n\r\n", 1)
    except ValueError:
        return "", "", {}, b""

    lines = head.decode("iso-8859-1").split("\r\n")
    if not lines or " " not in lines[0]:
        return "", "", {}, b""

    method, path, *_ = lines[0].split(" ")

    headers: Dict[str, str] = {}
    for line in lines[1:]:
        if ":" in line:
            k, v = line.split(":", 1)
            headers[k.strip().lower()] = v.strip()

    return method, path, headers, body


def handle_get(path: str) -> bytes:
    """Обработка GET-запросов."""
    if path == "/":
        data = data_store.get_all()
        disciplines = sorted(data.keys(), key=lambda s: s.lower())

        # Формируем строки таблицы
        rows = []
        for d in disciplines:
            grades = "; ".join(escape_html(g) for g in data[d])
            rows.append(f"<tr><td>{escape_html(d)}</td><td>{grades}</td></tr>")
        rows_html = "\n".join(rows) if rows else '<tr><td colspan="2">Пока пусто</td></tr>'

        # Читаем index.html
        try:
            with open("index.html", "r", encoding="utf-8") as f:
                template = f.read()
        except FileNotFoundError:
            return build_response("500 Internal Server Error", {}, "index.html not found")

        html = template.replace("{{rows}}", rows_html)
        return build_response("200 OK", {}, html)

    return build_response("404 Not Found", {}, "Not Found")


def _is_positive_number(text: str) -> bool:
    """
    Возвращает True, если строка — положительное число > 0.
    """
    norm = text.replace(",", ".")
    try:
        return float(norm) > 0.0
    except ValueError:
        return False


def handle_post(path: str, headers: Dict[str, str], body: bytes) -> bytes:
    """Обработка POST-запросов."""
    if path == "/add":
        if "application/x-www-form-urlencoded" not in headers.get("content-type", ""):
            return build_response("400 Bad Request", {}, "Expected x-www-form-urlencoded")

        form = urllib.parse.parse_qs(body.decode("utf-8"), keep_blank_values=True)
        discipline = (form.get("discipline", [""])[0]).strip()
        grade_raw = (form.get("grade", [""])[0]).strip()

        # Серверная проверка: положительное число > 0 (целое или дробное, . или ,)
        if discipline and _is_positive_number(grade_raw):
            data_store.add_grade(discipline, grade_raw)

        return build_response("303 See Other", {"Location": "/"}, "")

    return build_response("404 Not Found", {}, "Not Found")


def escape_html(s: str) -> str:
    """Экранирование спецсимволов в HTML."""
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
         .replace('"', "&quot;")
         .replace("'", "&#39;")
    )


def serve():
    """Главный цикл сервера."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen(5)
        print(f"Server running at http://{HOST}:{PORT}")

        while True:
            conn, _ = srv.accept()
            with conn:
                try:
                    raw = conn.recv(65535)
                    method, path, headers, body = parse_request(raw)
                    length = int(headers.get("content-length", "0"))
                    while len(body) < length:
                        chunk = conn.recv(65535)
                        if not chunk:
                            break
                        body += chunk
                except (socket.timeout, ValueError, UnicodeDecodeError):
                    conn.sendall(build_response("400 Bad Request", {}, "Bad Request"))
                    continue

                if method == "GET":
                    resp = handle_get(path)
                elif method == "POST":
                    resp = handle_post(path, headers, body)
                else:
                    resp = build_response("405 Method Not Allowed", {"Allow": "GET, POST"}, "Method Not Allowed")

                conn.sendall(resp)


if __name__ == "__main__":
    serve()
