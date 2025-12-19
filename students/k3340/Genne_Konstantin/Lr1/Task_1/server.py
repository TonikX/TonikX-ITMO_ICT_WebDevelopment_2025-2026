import socket

HOST = '127.0.0.1'
PORT = 9090

# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Привязываем сокет к адресу и порту
server_socket.bind((HOST, PORT))

print(f"Сервер запущен на {HOST}:{PORT}")

while True:
    # Получаем данные от клиента и его адрес
    client_data, client_address = server_socket.recvfrom(1024)
    print(f'Сообщение от клиента: {client_data.decode('utf-8')}')

    # Отправляем ответ клиенту
    message = 'Hello, client'
    server_socket.sendto(message.encode('utf-8'), client_address)