import socket

HOST = '127.0.0.1'
PORT = 9090

# Создаём сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Отправляем сообщение на сервер
message = 'Hello, server'
client_socket.sendto(message.encode('utf-8'), (HOST, PORT))

# Получаем ответ от сервера
server_data, server_address = client_socket.recvfrom(1024)
print(f'Ответ от сервера: {server_data.decode('utf-8')}')

# Закрываем сокет
client_socket.close()