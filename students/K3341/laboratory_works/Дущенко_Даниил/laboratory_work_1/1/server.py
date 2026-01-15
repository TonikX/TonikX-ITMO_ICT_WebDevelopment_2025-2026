import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('127.0.0.1', 9090))
print("Server start")

while True:
    data, addr = sock.recvfrom(1024)
    print(f"Client {addr}: {data.decode('utf-8')}")
    sock.sendto(b'Hello, client', addr)