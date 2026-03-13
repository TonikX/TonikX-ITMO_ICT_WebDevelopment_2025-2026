import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9999

# Создаем UDP-сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Отправляем сообщение серверу
message = "Hello, server"
client_socket.sendto(message.encode("utf-8"), (SERVER_HOST, SERVER_PORT))
print(f"Sent to server: {message}")

# Ждём ответ от сервера
data, addr = client_socket.recvfrom(4096)
reply = data.decode("utf-8")
print(f"Received from server {addr}: {reply}")

# Закрываем сокет, освобождаем ресурсы
client_socket.close()