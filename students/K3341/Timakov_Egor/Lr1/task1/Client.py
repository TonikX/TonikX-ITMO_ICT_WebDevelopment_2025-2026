import socket
import time

# Настройки клиента
serverHost = "127.0.0.1"
serverPort = 8080
message = "Hello Server"

# Создаем юдп сокет

ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Отправляем сообщение серверу
ClientSocket.sendto(message.encode(), (serverHost, serverPort))

data, _ = ClientSocket.recvfrom(1024)

print(f"Message from server : {data.decode()}")


time.sleep(120)

