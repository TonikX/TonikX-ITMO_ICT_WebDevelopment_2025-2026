import socket

# IP и порт сервера
HOST = "127.0.0.1"   # локальный адрес
PORT = 12345         # любой свободный порт

# Создаём UDP-сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print(f"Сервер запущен на {HOST}:{PORT} и ожидает сообщений...")

while True:
    # Принимаем coo
    data, addr = server_socket.recvfrom(1024)  # 1024 байта - буфер
    print(f"Получено сообщение от {addr}: {data.decode()}")

    # Отправляем ответ
    reply = "Hello, client"
    server_socket.sendto(reply.encode(), addr)
