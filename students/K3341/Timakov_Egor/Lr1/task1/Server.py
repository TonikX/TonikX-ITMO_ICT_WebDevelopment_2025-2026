import socket

# Настройки сервера
host = "127.0.0.1"
port = 8080
message = "Hello client"

# Создание юдп сокета
ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ServerSocket.bind((host, port))

print(f"Server has been started at {host}:{port}")

while True:
    data, address = ServerSocket.recvfrom(1024)
    print(f" Message from {address} : {data.decode()}")

    ServerSocket.sendto(message.encode(), address)

