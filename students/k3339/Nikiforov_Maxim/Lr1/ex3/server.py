import socket
from pathlib import Path

HOST = "0.0.0.0"
PORT = 8080
FILE = Path("./Lr1/ex3/Index.html")

def build_response(body: bytes, status: str = "200 OK", content_type="text/html; charset=utf-8") -> bytes:
    headers = [
        f"HTTP/1.1 {status}",
        f"Content-Type: {content_type}",
        f"Content-Length: {len(body)}",
        "Connection: close",
    ]
    head = ("\r\n".join(headers) + "\r\n\r\n").encode("utf-8")
    return head + body

def main():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Полезно при перезапуске сервера: порт освобождается без долгого TIME_WAIT
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(5)
    print(f"HTTP сервер запущен на http://localhost:{PORT} (файл: {FILE.resolve()})")

    try:
        while True:
            conn, addr = srv.accept()
            try:
                # Читаем первый кусок запроса (нам достаточно стартовой строки и заголовков)
                _ = conn.recv(1024)

                if FILE.exists():
                    body = FILE.read_bytes()
                    resp = build_response(body, "200 OK")
                else:
                    body = b"404 Not Found: index.html not found"
                    resp = build_response(body, "404 Not Found", content_type="text/plain; charset=utf-8")

                conn.sendall(resp)
            finally:
                conn.close()
    except KeyboardInterrupt:
        print("\nОстановка сервера...")
    finally:
        srv.close()

if __name__ == "__main__":
    main()