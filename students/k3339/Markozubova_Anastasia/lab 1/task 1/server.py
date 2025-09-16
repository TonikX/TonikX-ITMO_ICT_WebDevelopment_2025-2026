import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", 8080))

data, addr = sock.recvfrom(1024)
print(data.decode())

sock.sendto(b"Hello, client", addr)
sock.close()
