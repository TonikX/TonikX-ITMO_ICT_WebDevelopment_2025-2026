import socket

# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Привязываем сокет к адресу и порту
server_socket.bind((socket.gethostname(), 8080))

print("Сервер запущен на порту 8080...")

while True:
    # Получаем сообщение от клиента
    request, client_address = server_socket.recvfrom(1024)
    request = request.decode()
    print(f'Запрос от клиента {client_address}: {request}')

    # Отправляем ответ клиенту
    response = 'Hello, client!'
    server_socket.sendto(response.encode(), client_address)
