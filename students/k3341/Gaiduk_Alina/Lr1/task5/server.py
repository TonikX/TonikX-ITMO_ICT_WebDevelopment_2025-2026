import socket
import html
import json
from urllib.parse import parse_qs

grades = {}

DATA_FILE = "grades.json"
TEMPLATE_FILE = "index.html"


def load_data():
    global grades
    try:
        with open(DATA_FILE, encoding="utf-8") as f:
            grades = json.load(f)
    except FileNotFoundError:
        grades = {}

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(grades, f, ensure_ascii=False, indent=2)


def handle_request(request):
    try:
        line, *_ = request.split("\r\n")
        method, path, _ = line.split()
    except ValueError:
        return response("400 Bad Request", "Неверный запрос")

    if method == "GET" and path == "/":
        return generate_html()

    if method == "POST" and path == "/add":
        try:
            body = request.split("\r\n\r\n", 1)[1]
            data = parse_qs(body)
            subject = data.get("subject", [""])[0].strip()
            grade = data.get("grade", [""])[0].strip()

            if not subject or not grade.isdigit():
                raise ValueError

            grade_int = int(grade)
            if not (1 <= grade_int <= 5):
                raise ValueError

            # Добавляет ключ-значение в словарь
            grades.setdefault(subject, []).append(grade_int)
            save_data()

            # Редиректим после POST
            return response("303 See Other", "", {"Location": "/"})

        except Exception:
            return response("400 Bad Request", "Неверные данные")

    return response("404 Not Found", "Страница не найдена")


def generate_html():
    try:
        with open(TEMPLATE_FILE, encoding="utf-8") as f:
            template = f.read()
    except FileNotFoundError:
        return response("500 Internal Server Error", "Нет шаблона")

    rows = []
    for subj, marks in grades.items():
        safe_subj = html.escape(subj)
        marks_str = ", ".join(map(str, marks))
        rows.append(f"<tr><td>{safe_subj}</td><td>{marks_str}</td></tr>")

    table = "\n".join(rows) or "<tr><td colspan=2><em>Пока пусто</em></td></tr>"
    html_page = template.replace("{{rows}}", table)

    return response("200 OK", html_page, {
        "Content-Type": "text/html; charset=utf-8"
    })


def response(status, body, headers=None):
    headers = headers or {}
    body_bytes = body.encode("utf-8")
    headers["Content-Length"] = str(len(body_bytes))
    headers.setdefault("Content-Type", "text/plain; charset=utf-8")

    head = "".join(f"{k}: {v}\r\n" for k, v in headers.items())
    return f"HTTP/1.1 {status}\r\n{head}\r\n{body}"


def run_server():
    load_data()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("127.0.0.1", 11111))
        server_socket.listen()
        print(f"Сервер запущен: http://127.0.0.1:11111")
        while True:
            client_socket, _ = server_socket.accept()
            with client_socket:
                req = client_socket.recv(4096).decode("utf-8")
                resp = handle_request(req)
                client_socket.sendall(resp.encode("utf-8"))


if __name__ == "__main__":
    run_server()
