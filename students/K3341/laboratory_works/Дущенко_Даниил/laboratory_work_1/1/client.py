import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(b'Hello, server', ('127.0.0.1', 9090))
data, _ = sock.recvfrom(1024)
print(f"Server: {data.decode('utf-8')}")
sock.close()