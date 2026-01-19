import socket

# Параметры сервера
HOST = 'localhost'  # Адрес хоста (localhost для локальных соединений)
PORT = 8080         # Порт, на котором будет работать сервер

# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Привязываем сокет к адресу и порту
server_socket.bind((HOST, PORT))

print(f"UDP сервер запущен на {HOST}:{PORT}...")

while True:
    # Принимаем соединение, запрос от клиента
    request, client_address = server_socket.recvfrom(1024)
    print(f'Подключение от {client_address}')
    print(f'Запрос клиента:\n{request.decode("utf-8")}')

    response = 'Hello, client'

    # Отправляем ответ клиенту
    server_socket.sendto(response.encode("utf-8"), client_address)
