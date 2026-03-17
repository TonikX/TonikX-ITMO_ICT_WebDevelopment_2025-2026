import socket

HOST = "127.0.0.1"
PORT = 1996

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"HTTP is running on http://{HOST}:{PORT}")

while True:
    conn, addr = server_socket.accept()
    print("Connected:", addr)

    request = conn.recv(1024).decode()
    print("=== HTTP Request ===")
    print(request)

    # Загрузка HTML из файла
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            body = f.read()
    except FileNotFoundError:
        body = "<html><body><h1>File index.html is not found</h1></body></html>"

    # Формирование HTTP-ответа
    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body.encode())}\r\n"
        "\r\n"
        f"{body}"
    )

    conn.sendall(response.encode())
    conn.close()
