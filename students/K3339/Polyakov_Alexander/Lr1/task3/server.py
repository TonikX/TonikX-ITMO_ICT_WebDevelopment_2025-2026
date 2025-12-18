import socket
import os
from datetime import datetime
from email.utils import formatdate

HOST = "127.0.0.1"
PORT = 8080
ENC = "utf-8"

INDEX_FILE = "index.html"
MAX_REQ_BYTES = 64 * 1024  # защитимся от очень длинных запросов

def build_response(status: str, body: bytes, content_type: str = "text/html; charset=utf-8") -> bytes:
    """Формируем HTTP/1.1-ответ с обязательными заголовками."""
    lines = [
        f"HTTP/1.1 {status}",
        f"Date: {formatdate(timeval=None, usegmt=True)}",
        "Server: MinimalSocketServer/1.0",
        f"Content-Length: {len(body)}",
        f"Content-Type: {content_type}",
        "Connection: close",
        "",  # пустая строка = конец заголовков
        ""
    ]
    headers = "\r\n".join(lines).encode("ascii")
    return headers + body


def handle_client(conn: socket.socket, addr):
    with conn:
        request = conn.recv(1024).decode()
        print(f'Request from {addr}:\n{request}')

        if os.path.exists(INDEX_FILE) and os.path.isfile(INDEX_FILE):
            with open(INDEX_FILE, "rb") as f:
                body = f.read()
            resp = build_response("200 OK", body, "text/html; charset=utf-8")
        else:
            body = (
                "<!doctype html><html><head><meta charset='utf-8'>"
                "<title>404 Not Found</title></head><body>"
                "<h1>404 Not Found</h1><p>index.html не найден.</p>"
                "</body></html>"
            ).encode(ENC)
            resp = build_response("404 Not Found", body, "text/html; charset=utf-8")

        conn.sendall(resp)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:

        srv.bind((HOST, PORT))
        srv.listen(50)  # очередь полу-соединений; обслуживаем всё равно последовательно
        print(f"HTTP-server listens on http://{HOST}:{PORT}")
        try:
            while True:
                # Accept connection
                conn, addr = srv.accept()
                handle_client(conn, addr)
        except KeyboardInterrupt:
            print("\nShutting down...")

if __name__ == "__main__":
    main()
