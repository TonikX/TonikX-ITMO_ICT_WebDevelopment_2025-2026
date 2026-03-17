import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 30114

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = "Hello, server"
sock.sendto(message.encode(), (SERVER_HOST, SERVER_PORT))
print(f"Sent to the server: {message}")

data, addr = sock.recvfrom(1996)
print(f"The answer from server: {data.decode()}")

sock.close()