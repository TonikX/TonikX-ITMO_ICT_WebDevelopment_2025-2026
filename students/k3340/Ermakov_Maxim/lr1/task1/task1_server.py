import socket

# На каком адресе и порту слушаем
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8080

# Создаём UDP-сокет: AF_INET (IPv4), SOCK_DGRAM (UDP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Привязываем сокет к адресу/порту, чтобы принимать датаграммы
server_socket.bind((SERVER_HOST, SERVER_PORT))
print(f"UDP-сервер запущен на {SERVER_HOST}:{SERVER_PORT}")
print("Ожидаю сообщения от клиента... (Ctrl+C для выхода)\n")

try:
    while True:
        # recvfrom возвращает (данные, адрес_клиента)
        data, client_addr = server_socket.recvfrom(1024)  # до 1024 байт
        message = data.decode("utf-8", errors="ignore")
        print(f"Получено от {client_addr}: {message}")

        # Формируем ответ
        reply = "Hello, client"
        server_socket.sendto(reply.encode("utf-8"), client_addr)
        print(f"Отправлен ответ клиенту {client_addr}: {reply}\n")

except KeyboardInterrupt:
    print("\nСервер остановлен пользователем.")
finally:
    server_socket.close()
