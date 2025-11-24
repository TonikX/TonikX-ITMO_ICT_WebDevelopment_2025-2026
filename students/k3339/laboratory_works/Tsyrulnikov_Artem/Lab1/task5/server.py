import socket
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import parse_qs


class Config:
    HOST = "0.0.0.0"
    PORT = 8005
    BUFFER_SIZE = 4096
    TEMPLATE_FILE = "template.html"
    BASE = Path(__file__).parent


@dataclass(frozen=True)
class HTTPRequest:
    METHOD: str | None = None
    PATH: str | None = None
    BODY: str | None = None


grades = {}


def load_template() -> str:
    try:
        return (Config.BASE / Config.TEMPLATE_FILE).read_text(encoding="utf-8")
    except Exception as e:
        return f"<h1>500 - Ошибка загрузки шаблона: {e}</h1>"


def parse_http_request(request: str) -> HTTPRequest:
    lines = request.split("\r\n")
    if not lines or len(lines[0].split()) < 2:
        return HTTPRequest()

    method, path = lines[0].split()[:2]
    body = request.split("\r\n\r\n", 1)[1] if "\r\n\r\n" in request else ""
    return HTTPRequest(method, path, body)


def parse_form_data(body: str) -> dict:
    parsed = parse_qs(body)
    return {key: values[0] if values else "" for key, values in parsed.items()}


def render_response(content: str, status: str = "200 OK") -> bytes:
    return (
        f"HTTP/1.1 {status}\r\n"
        f"Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(content.encode('utf-8'))}\r\n"
        f"Connection: close\r\n\r\n{content}"
    ).encode("utf-8")


def render_redirect(location: str = "/") -> bytes:
    return (f"HTTP/1.1 302 Found\r\nLocation: {location}\r\nConnection: close\r\n\r\n").encode("utf-8")


def generate_page() -> str:
    template = load_template()

    rows = (
        '<tr><td colspan="3" style="text-align: center; color: #666;">Оценки не найдены</td></tr>'
        if not grades
        else "".join(
            f"<tr><td>{i}</td><td>{subject}</td><td>{', '.join(map(str, grade_list))}</td></tr>"
            for i, (subject, grade_list) in enumerate(grades.items(), 1)
        )
    )

    return template.replace("{grades_rows}", rows)


def validate_and_add_grade(data: dict) -> str | None:
    subject = data.get("subject", "").strip()
    grade_str = data.get("grade", "").strip()

    if not subject or not grade_str:
        return "Все поля должны быть заполнены"

    try:
        grade = int(grade_str)
    except ValueError:
        return "Некорректная оценка"

    if not 1 <= grade <= 5:
        return "Оценка должна быть от 1 до 5"

    if subject not in grades:
        grades[subject] = []
    grades[subject].append(grade)
    print(f"Добавлена оценка: {subject} - {grade}")
    return None


def handle_request(method: str | None, path: str | None, body: str | None) -> bytes:
    if method == "GET":
        if path not in {"/"}:
            return render_response("<h1>404 - Страница не найдена</h1>", "404 Not Found")
        return render_response(generate_page())

    if method == "POST":
        if path != "/":
            return render_response("<h1>404 - Страница не найдена</h1>", "404 Not Found")

        if not body:
            return render_response("<h1>400 - Отсутствует тело запроса</h1>", "400 Bad Request")

        data = parse_form_data(body)
        error = validate_and_add_grade(data)
        if error:
            return render_response(f"<h1>Ошибка: {error}</h1>", "400 Bad Request")

        return render_redirect("/")

    return render_response("<h1>405 - Метод не поддерживается</h1>", "405 Method Not Allowed")


def handle_client(client_socket: socket.socket, client_address: tuple) -> None:
    data = client_socket.recv(Config.BUFFER_SIZE)
    request = data.decode("utf-8")

    method = request.split()[0] if request.split() else ""
    if method == "POST":
        if "Content-Length:" not in request:
            error_response = render_response("<h1>400 - Отсутствует Content-Length</h1>", "400 Bad Request")
            client_socket.send(error_response)
            print(f"{client_address[0]}:{client_address[1]} <- 400 Bad Request")
            return

        # Извлекаем Content-Length из заголовков
        lines = request.split("\r\n")
        content_length = 0
        for line in lines:
            if line.lower().startswith("content-length:"):
                content_length = int(line.split(":")[1].strip())
                break

        # Проверяем, есть ли уже тело в запросе
        if "\r\n\r\n" in request:
            body_start = request.find("\r\n\r\n") + 4
            existing_body = request[body_start:]
            body_bytes_received = len(existing_body.encode("utf-8"))

            # Если нужно дочитать тело
            while body_bytes_received < content_length:
                additional_data = client_socket.recv(Config.BUFFER_SIZE)
                request += additional_data.decode("utf-8")
                body_bytes_received += len(additional_data)

    request = parse_http_request(request)
    print(f"{client_address[0]}:{client_address[1]} -> {request.METHOD} {request.PATH}")

    http_response = handle_request(request.METHOD, request.PATH, request.BODY)
    client_socket.send(http_response)
    print(f"{client_address[0]}:{client_address[1]} <- {http_response[:15]}")


def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((Config.HOST, Config.PORT))
    server_socket.listen(5)
    print(f"Сервер запущен на {Config.HOST}:{Config.PORT}")
    print(f"Ссылка: http://localhost:{Config.PORT}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Подключение от {client_address[0]}:{client_address[1]}")

            try:
                handle_client(client_socket, client_address)
            except Exception as e:
                error_response = render_response(f"<h1>500 - Ошибка сервера: {str(e)}</h1>")

                client_socket.send(error_response)
                print(f"{client_address[0]}:{client_address[1]} <- {error_response[:15]}")

            finally:
                client_socket.close()

    except KeyboardInterrupt:
        print("\nЗавершение работы сервера...")

    finally:
        server_socket.close()
        print("Сервер остановлен")


if __name__ == "__main__":
    run_server()
