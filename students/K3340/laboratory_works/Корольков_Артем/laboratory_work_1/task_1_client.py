import socket

# Создаем UDP-сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Адрес сервера
server_address = ('localhost', 12345)

# Сообщение для отправки
message = "Hello, server"
client_socket.sendto(message.encode('utf-8'), server_address)
print(f"Отправлено сообщение серверу: {message}")

# Получаем ответ от сервера
data, _ = client_socket.recvfrom(1024)
print(f"Получен ответ от сервера: {data.decode('utf-8')}")

# Закрываем сокет
client_socket.close()