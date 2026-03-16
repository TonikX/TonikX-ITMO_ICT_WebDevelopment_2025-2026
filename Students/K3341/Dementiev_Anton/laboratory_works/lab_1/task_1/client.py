import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 12345)

message = "Hello, server"
client_socket.sendto(message.encode(), server_address)

data, server = client_socket.recvfrom(1024)
print("Ответ от сервера:", data.decode())

client_socket.close()
