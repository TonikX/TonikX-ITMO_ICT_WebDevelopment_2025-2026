import socket
from config import HOST, PORT

msg = "Hello, server"
conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
conn.connect((HOST, PORT))
conn.send(msg.encode())
response = conn.recv(1024)
print(f"response: {response.decode("utf-8")}")