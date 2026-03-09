import socket

# Создаём  сокет клиента для UDP-подключения
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Адрес сервера
server_address = ('localhost', 8080)

# Отправляем запрос серверу
message = 'Hello, server'
client_socket.sendto(message.encode(), server_address)
print(f'Отправлено серверу: {message}')

# Получаем ответ от сервера
response, server = client_socket.recvfrom(1024)
print(f'Ответ от сервера: {response.decode()}')

# Закрываем сокет
client_socket.close()
