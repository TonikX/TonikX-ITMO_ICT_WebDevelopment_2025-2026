import socket

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost", 9999))
print("Server is running...")
data, addr = server.recvfrom(1024)
print(f"Client: {data.decode()}")
server.sendto("Hello, client".encode(), addr)
server.close()
