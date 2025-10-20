import socket

# Параметры сервера
SERVER_HOST = "localhost"
SERVER_PORT = 8080

# Создаем UDP-сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Сообщение для сервера
message = "Hello, server"
client_socket.sendto(message.encode(), (SERVER_HOST, SERVER_PORT))

# Ждем ответ от сервера
data, server = client_socket.recvfrom(1024)
print("Ответ от сервера:", data.decode())

# Закрываем сокет
client_socket.close()
