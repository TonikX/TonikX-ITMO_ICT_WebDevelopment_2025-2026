import socket

# Параметры сервера
HOST = "localhost"   # или "127.0.0.1"
PORT = 8080          # порт, который слушает сервер

# Создаем UDP-сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print(f"UDP сервер запущен на {HOST}:{PORT}...")

while True:
    # Получаем сообщение от клиента
    data, client_address = server_socket.recvfrom(1024)  # ждем данные (макс. 1024 байта)
    message = data.decode()
    print(f"Сообщение от клиента {client_address}: {message}")

    # Отправляем ответ клиенту
    response = "Hello, client"
    server_socket.sendto(response.encode(), client_address)
