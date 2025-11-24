import os
import socket
from pathlib import Path


class Config:
    HOST = "0.0.0.0"
    PORT = 8003
    BUFFER_SIZE = 1024
    HTML_FILE = "index.html"
    BASE = Path(os.path.dirname(os.path.abspath(__file__)))


def load_html_file() -> str:
    try:
        with open(Config.BASE / Config.HTML_FILE, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        return f"<h1>500 - Ошибка сервера: {e}</h1>"


def render_response(html_content: str) -> str:
    content_length = len(html_content.encode("utf-8"))
    response_headers = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {content_length}\r\n"
        "Connection: close\r\n"
        "\r\n"
    )
    return response_headers + html_content


def parse_http_request(request: str) -> tuple[str, str]:
    lines = request.split("\r\n")
    if not lines:
        return "", ""

    request_line = lines[0]
    parts = request_line.split(" ")

    if len(parts) < 2:
        return "", ""

    method = parts[0]
    path = parts[1]
    return method, path


def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((Config.HOST, Config.PORT))
    server_socket.listen(5)
    print(f"Cервер запущен на {Config.HOST}:{Config.PORT}")
    print(f"Ссылка: http://localhost:{Config.PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Подключение от {client_address[0]}:{client_address[1]}")

        try:
            data = client_socket.recv(Config.BUFFER_SIZE)
            request = data.decode("utf-8")

            method, path = parse_http_request(request)
            if method and path:
                print(f"{client_address[0]}:{client_address[1]} -> {method} {path}")

            html_content = load_html_file()
            http_response = render_response(html_content)

            client_socket.send(http_response.encode("utf-8"))
            print(f"{client_address[0]}:{client_address[1]} <- {http_response[:15]}")

        except Exception as e:
            error_response = render_response(f"<h1>500 - Ошибка сервера: {e}</h1>")
            client_socket.send(error_response.encode("utf-8"))
            print(f"{client_address[0]}:{client_address[1]} <- {error_response[:15]}")

        finally:
            client_socket.close()


if __name__ == "__main__":
    run_server()
