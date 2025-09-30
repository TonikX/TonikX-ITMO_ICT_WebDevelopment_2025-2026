import socket

# Адрес и порт серва
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = "Hello, server"
client_socket.sendto(message.encode(), (SERVER_HOST, SERVER_PORT))
print(f"Отправлено сообщение серверу: {message}")

data, addr = client_socket.recvfrom(1024)
print(f"Ответ от сервера: {data.decode()}")

client_socket.close()
