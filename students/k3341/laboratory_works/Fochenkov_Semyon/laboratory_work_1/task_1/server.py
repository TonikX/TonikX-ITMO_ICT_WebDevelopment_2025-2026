import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 12345)
server_socket.bind(server_address)

print("Сервер запущен и ожидает сообщения...")

data, client_address = server_socket.recvfrom(1024)
print("Сообщение от клиента:", data.decode())

message = "Hello, client"
server_socket.sendto(message.encode(), client_address)

print("Ответ отправлен клиенту.")

server_socket.close()
