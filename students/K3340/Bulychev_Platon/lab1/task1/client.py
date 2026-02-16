import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto("Hello, server".encode(), ("localhost", 9999))
data, _ = client.recvfrom(1024)
print(f"Server: {data.decode()}")
client.close()
