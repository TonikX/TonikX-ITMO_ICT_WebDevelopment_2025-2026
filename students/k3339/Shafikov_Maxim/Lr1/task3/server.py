import socket
import os
from students.k3339.Shafikov_Maxim.Lr1.config import host, port


if __name__ == "__main__":
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_socket.bind((host, port))
    tcp_socket.listen(5)

    print(f"Сервер запущен на http://{host}:{port}")

    while True:
        conn, addr = tcp_socket.accept()
        with conn:
            request = conn.recv(1024).decode("utf-8", errors="ignore")
            print(f"\n--- Запрос от {addr} ---")
            print(request)

            if os.path.exists("index.html"):
                with open("index.html", "r", encoding="utf-8") as f:
                    body = f.read()
                response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html; charset=utf-8\r\n"
                    f"Content-Length: {len(body.encode('utf-8'))}\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                    f"{body}"
                )
            else:
                body = "<h1>Файл index.html не найден</h1>"
                response = (
                    "HTTP/1.1 404 Not Found\r\n"
                    "Content-Type: text/html; charset=utf-8\r\n"
                    f"Content-Length: {len(body.encode('utf-8'))}\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                    f"{body}"
                )

            conn.sendall(response.encode("utf-8"))
