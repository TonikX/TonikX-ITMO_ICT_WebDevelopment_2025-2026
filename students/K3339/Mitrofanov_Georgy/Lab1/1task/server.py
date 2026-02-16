import socket

# Сервер слушает конкретный IP и порт
HOST = "127.0.0.1"
PORT = 9999

# AF_INET = IPv4, SOCK_DGRAM = UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# bind = "занять" адрес/порт, чтобы принимать UDP-пакеты
server_socket.bind((HOST, PORT))

print(f"UDP server started on {HOST}:{PORT}")
print("Waiting for message...")

while True:
    # recvfrom возвращает (данные, адрес_клиента)
    data, client_addr = server_socket.recvfrom(4096)

    # UDP присылает байты, переводим в строку
    message = data.decode("utf-8")
    print(f"Received from {client_addr}: {message}")

    # Отправляем ответ туда же (на адрес клиента)
    reply = "Hello, client"
    server_socket.sendto(reply.encode("utf-8"), client_addr)
    print(f"Sent to {client_addr}: {reply}")
