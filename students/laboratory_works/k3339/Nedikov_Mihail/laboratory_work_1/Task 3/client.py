import socket

# TCP-клиент устанавливает HTTP-соединение и отправляет GET-запрос.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключаемся к локальному серверу.
client_socket.connect(("localhost", 8080))

# Формируем минимальный HTTP-запрос и отправляем его.
request = "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"
client_socket.sendall(request.encode())

# Получаем ответ сервера и показываем его целиком.
response = client_socket.recv(1024).decode()

print("=== Ответ сервера ===")
print(response)

# Закрываем соединение.
client_socket.close()
