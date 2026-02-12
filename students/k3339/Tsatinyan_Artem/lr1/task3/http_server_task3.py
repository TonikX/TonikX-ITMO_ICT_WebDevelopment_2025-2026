import socket
from datetime import datetime

HOST = "127.0.0.1"
PORT = 8080
ENC = "utf-8"

INDEX_FILE = "index.html"

def http_response(status_line: str, headers: dict, body: bytes) -> bytes:
    """
    Формируем полный HTTP-ответ.
    Аргументы:
      - status_line: строка статуса (например, "HTTP/1.1 200 OK")
      - headers: словарь HTTP-заголовков
      - body: тело ответа (в байтах)
    """
    # Статус + заголовки
    head = status_line + "\r\n"
    for k, v in headers.items():
        head += f"{k}: {v}\r\n"
    head += "\r\n"
    return head.encode(ENC) + body

# Парсинг запроса и отправка ответа.
def handle_client(conn, addr):
    try:
        # Читаем сырой HTTP запрос
        raw = conn.recv(65536)
        if not raw:
            return

        # Декодируем запрос в строку
        req = raw.decode(ENC, errors="replace")

        # Первая строка HTTP-запроса: METHOD SP PATH SP HTTP/VERSION
        request_line = req.split("\r\n", 1)[0]
        parts = request_line.split()
        method = parts[0] if len(parts) > 0 else ""
        path = parts[1] if len(parts) > 1 else "/"

        print(f"[{datetime.now()}] {addr} -> {request_line}")

        # Отдаём только / или /index.html
        if path == "/" or path == "/index.html":

            # Читаем содержимое index.html и отправляем
            with open(INDEX_FILE, "rb") as f:
                body = f.read()
            resp = http_response(
                "HTTP/1.1 200 OK",
                {
                    "Content-Type": "text/html; charset=UTF-8",
                    "Content-Length": str(len(body)),
                    "Connection": "close",
                },
                body,
            )
            conn.sendall(resp)
        else:
            # Любой другой путь -> 404
            body = b"<h1>404 Not Found</h1>"
            resp = http_response(
                "HTTP/1.1 404 Not Found",
                {
                    "Content-Type": "text/html; charset=UTF-8",
                    "Content-Length": str(len(body)),
                    "Connection": "close",
                },
                body,
            )
            conn.sendall(resp)
    finally:
        try:
            conn.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        print(f"HTTP-сервер слушает на http://{HOST}:{PORT} (GET / -> {INDEX_FILE})")
        # Разрешаем быстрое переподключение
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen(10)  # Очередь до 10 подключений
        while True:
            conn, addr = srv.accept()
            handle_client(conn, addr)

if __name__ == "__main__":
    main()
