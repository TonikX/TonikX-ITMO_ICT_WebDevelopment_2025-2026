import socket

HOST = 'localhost'
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    server_socket.bind((HOST, PORT))
    print(f"UDP сервер запущен на {HOST}:{PORT}...")
    while True:
        data, addr = server_socket.recvfrom(1024)
        msg = data.decode('utf-8', errors='ignore')
        print(f"Получено от {addr}: {msg}")
        server_socket.sendto(b"Hello, client", addr)
        server_socket.close()
        break
