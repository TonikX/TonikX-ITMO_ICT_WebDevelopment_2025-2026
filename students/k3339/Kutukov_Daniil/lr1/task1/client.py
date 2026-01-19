import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = "Hello, server"
client_socket.sendto(message.encode("utf-8"), (SERVER_HOST, SERVER_PORT))

data, _ = client_socket.recvfrom(1024)
print("Ответ от сервера:", data.decode("utf-8"))

client_socket.close()