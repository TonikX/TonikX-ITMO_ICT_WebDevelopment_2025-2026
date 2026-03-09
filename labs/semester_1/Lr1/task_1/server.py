import socket

# Создаём сокет сервера для UDP-подключения
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Запускаем сервер на localhost
server_socket.bind(('localhost', 8080))
print("UDP-сервер запущен на порту 8080...")

# Запускаем цикл работы сервера
while True:

    # Получаем UDP-запрос от клиента
    data, client_address = server_socket.recvfrom(1024)
    message = data.decode()
    print(f'Получено от {client_address}: {message}')

    # Посылаем UDP-ответ клиенту
    response = 'Hello, client'
    server_socket.sendto(response.encode(), client_address)
    print(f'Отправлен ответ: {response}')
