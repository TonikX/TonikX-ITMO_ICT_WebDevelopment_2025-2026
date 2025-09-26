import socket

# Создаем UDP сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Адрес сервера
server_address = ('localhost', 12345)

# Сообщение для отправки
message = "Hello, server"
print(f"Отправляем сообщение серверу: {message}")

# Отправляем сообщение серверу
client_socket.sendto(message.encode('utf-8'), server_address)

# Получаем ответ от сервера
response_data, server_addr = client_socket.recvfrom(1024)
response = response_data.decode('utf-8')

print(f"Получен ответ от сервера: {response}")

# Закрываем сокет
client_socket.close()
