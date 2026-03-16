import socket
import time

# Server settings
serverHost = "127.0.0.1"
serverPort = 8080

# Message
message = "Hello Server"

ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send msg
ClientSocket.sendto(message.encode(), (serverHost, serverPort))

# Receive msg
data, _ = ClientSocket.recvfrom(1024)

print(f"Message from server : {data.decode()}")

time.sleep(120)
