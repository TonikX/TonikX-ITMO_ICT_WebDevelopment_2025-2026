import socket

HOST = "127.0.0.1"
PORT = 8081

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.sendto(b"Hello, server!", (HOST, PORT))
    data, addr = s.recvfrom(4096)
    print("Server replied:", data.decode())