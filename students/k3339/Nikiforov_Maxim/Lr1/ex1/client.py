import socket

HOST = 'localhost'
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
    client_socket.settimeout(2.0)
    client_socket.sendto(b"Hello, server", (HOST, PORT))
    data, addr = client_socket.recvfrom(1024)
    print(f"Ответ от сервера: {data.decode('utf-8', errors='ignore')}")

