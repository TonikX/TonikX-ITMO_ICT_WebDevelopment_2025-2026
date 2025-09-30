import socket
import threading

HOST = "127.0.0.1"
PORT = 5005

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print(f"UDP сервер запущен на {HOST}:{PORT}")

def handle_client(data, addr):
    print(f"Клиент {addr} сказал:", data.decode())
    reply = "Hello, client"
    server_socket.sendto(reply.encode(), addr)

while True:
    data, addr = server_socket.recvfrom(1024)
    thread = threading.Thread(target=handle_client, args=(data, addr))
    thread.start()
