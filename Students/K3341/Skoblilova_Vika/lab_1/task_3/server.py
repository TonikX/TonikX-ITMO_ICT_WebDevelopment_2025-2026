import socket

HOST = "127.0.0.1"
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Сервер запущен на http://{HOST}:{PORT}")

while True:
    conn, addr = server_socket.accept()
    print(f"Подключился клиент {addr}")

    request = conn.recv(1024).decode()
    print("Запрос:\n", request)

    try:
        with open("index.html", "r", encoding="utf-8") as f:
            body = f.read()
    except FileNotFoundError:
        body = "<h1>Файл index.html не найден</h1>"

    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body.encode('utf-8'))}\r\n"
        "Connection: close\r\n"
        "\r\n"
        f"{body}"
    )

    conn.sendall(response.encode("utf-8"))
    conn.close()
