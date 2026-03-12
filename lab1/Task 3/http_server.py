import socket

# Настройки сервера
HOST = 'localhost'  # Сервер будет работать на локальной машине
PORT = 8080         # Порт для подключения клиентов

# Создаем TCP-сокет (для HTTP нужен TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к адресу и порту
server_socket.bind((HOST, PORT))

# Начинаем слушать входящие соединения, максимум 1 в очереди
server_socket.listen(1)

print(f"HTTP сервер запущен на http://{HOST}:{PORT}")

while True:
    # Ожидаем подключение клиента
    client_connection, client_address = server_socket.accept()
    print(f"Подключение от {client_address}")

    # Получаем HTTP-запрос от клиента
    request = client_connection.recv(1024).decode()
    print("Запрос клиента:")
    print(request)

    # Читаем содержимое HTML-файла для ответа
    with open("/Users/glavnipopivy/UCHEBA/web-prog/TonikX-ITMO_ICT_WebDevelopment_2025-2026/lab1/Task 3/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    # Формируем HTTP-ответ
    response = (
        "HTTP/1.1 200 OK\r\n"                         # Статус ответа
        "Content-Type: text/html; charset=utf-8\r\n"  # Тип контента
        f"Content-Length: {len(html_content.encode())}\r\n"  # Длина содержимого
        "\r\n"                                        # Пустая строка отделяет заголовки от тела
        f"{html_content}"                             # Тело ответа (HTML)
    )

    # Отправляем ответ клиенту
    client_connection.sendall(response.encode())

    # Закрываем соединение с клиентом
    client_connection.close()
