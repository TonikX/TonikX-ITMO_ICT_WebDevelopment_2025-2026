import socket

HOST = "127.0.0.1" 
PORT = 12345        

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print(f"Сервер запущен на {HOST}:{PORT} и ждет сообщения...")

while True:
    data, addr = server_socket.recvfrom(1024)
    message = data.decode("utf-8")
    print(f"Получено от клиента {addr}: {message}")

    if message == "Hello, server":
        reply = "Hello, client"
        server_socket.sendto(reply.encode("utf-8"), addr)
