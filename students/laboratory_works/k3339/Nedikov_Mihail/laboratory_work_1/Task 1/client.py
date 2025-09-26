import socket

# UDP-клиент отправляет текст и печатает ответ от сервера.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Формируем и отправляем запрос серверу.
request = "Hello, server"
client_socket.sendto(request.encode(), ("localhost", 8080))

# Получаем ответ и выводим его в консоль.
response, address = client_socket.recvfrom(1024)

print(response.decode())
