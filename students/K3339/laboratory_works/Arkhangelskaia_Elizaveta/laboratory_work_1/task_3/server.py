import socket

def http_server():
    host = "localhost"
    port = 8080
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)  # очередь на 5 подключений

    print(f"Сервер запущен: http://{host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"\nКлиент подключился: {client_address}")

        request = client_socket.recv(1024).decode("utf-8")
        print("Запрос:\n", request)

        try:
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
        except FileNotFoundError:
            response = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                "Connection: close\r\n"
                "\r\n"
                "<h1>404 — Файл index.html не найден</h1>"
            )

        client_socket.sendall(response.encode("utf-8"))
        client_socket.close()

if __name__ == "__main__":
    http_server()
