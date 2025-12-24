import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Отправляем сообщение серверу
message = 'Hello, server'
client_socket.sendto(message.encode(), ('localhost', 8080))

# Получаем ответ
data, server_address = client_socket.recvfrom(1024)
print(f'Ответ от сервера: {data.decode()}')

client_socket.close()
