import socket

# Создаем UDP-сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Отправляем сообщение серверу
message = "Hello, server"
client_socket.sendto(message.encode(), ('localhost', 8080))

# Получаем ответ от сервера
data, server_address = client_socket.recvfrom(1024)
print(f"Ответ от сервера: {data.decode()}")

# Закрываем сокет
client_socket.close()
