import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

HOST = 'localhost'
PORT = 8080

sock.sendto(b'Hello, server!', (HOST, PORT))

data, addr = sock.recvfrom(1024)
sock.close()

print(data.decode())
