import socket

server_address = ('localhost', 8080)

# Создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Отправляем сообщение серверу
client_socket.sendto("Hello, server".encode("utf-8"), server_address)

# Получаем ответ от сервера
data, _ = client_socket.recvfrom(1024)
print(f'Ответ от сервера: {data.decode("utf-8")}')

client_socket.close()