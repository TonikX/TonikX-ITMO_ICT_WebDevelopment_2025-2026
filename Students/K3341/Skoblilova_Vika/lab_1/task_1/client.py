import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5005

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = "Hello, server"
client_socket.sendto(message.encode(), (SERVER_HOST, SERVER_PORT))

data, _ = client_socket.recvfrom(1024)
print("Сервер ответил:", data.decode())

client_socket.close()
