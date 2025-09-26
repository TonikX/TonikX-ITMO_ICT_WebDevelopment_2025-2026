import socket
import os

# Адрес, на котором запускаем HTTP-сервер.
HOST = "localhost"
PORT = 8080

# Создаем TCP-сокет и переводим его в режим прослушивания.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

# Папка с index.html, который будем отдавать клиенту.
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "index.html")

while True:
    # Принимаем клиента и выводим информацию о подключении.
    client_connection, client_address = server_socket.accept()
    print(f"Подключился клиент {client_address}")

    # Читаем первый запрос и показываем его в консоли.
    request = client_connection.recv(1024).decode()
    print(f"Запрос клиента:\n{request}")

    # Читаем HTML-файл и формируем HTTP-ответ.
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    http_response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=UTF-8\r\n"
        f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
        "Connection: close\r\n"
        "\r\n"
        + html_content
    )

    # Отправляем ответ и закрываем соединение.
    client_connection.sendall(http_response.encode("utf-8"))
    client_connection.close()
