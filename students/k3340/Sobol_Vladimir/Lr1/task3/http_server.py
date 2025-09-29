import socket
import os

HOST = "localhost"
PORT = 8080

# Загружаем HTML из файла
with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Создаём TCP-сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"HTTP сервер запущен на {HOST}:{PORT}...")

while True:
    conn, addr = server_socket.accept()
    print(f"Подключение от {addr}")

    # Получаем запрос от клиента 
    request = conn.recv(1024).decode()
    print("Запрос:\n", request)

    # Формируем HTTP-ответ
    http_response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=UTF-8\r\n"
        f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
        "Connection: close\r\n"
        "\r\n"
        + html_content
    )

    # Отправляем ответ клиенту
    conn.sendall(http_response.encode("utf-8"))
    conn.close()


