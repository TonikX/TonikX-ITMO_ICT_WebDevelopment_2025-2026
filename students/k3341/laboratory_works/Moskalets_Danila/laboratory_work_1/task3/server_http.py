import socket

HOST = '127.0.0.1'
PORT = 9090

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"HTTP сервер запущен на http://{HOST}:{PORT}")

while True:
    conn, addr = server_socket.accept()
    print(f"Подключился клиент: {addr}")

    request = conn.recv(1024).decode('utf-8')
    print("Получен запрос:")
    print(request)

    # загружаем html из файла
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            body = f.read()

        # формируем http-ответ
        response = (
            "HTTP/1.1 200 OK\r\n" # код состояния 
            "Content-Type: text/html; charset=utf-8\r\n" # заголовки
            f"Content-Length: {len(body.encode('utf-8'))}\r\n" # заголовки
            "\r\n"
            f"{body}" # тело ответа
        )
    except FileNotFoundError:
        response = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            "\r\n"
            "<h1>404 Файл не найден</h1>"
        )

    conn.sendall(response.encode('utf-8'))
    conn.close()