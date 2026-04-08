import socket

# Конфигурация клиента 
SERVER_HOST = "127.0.0.1"  # локальный хост (localhost)
SERVER_PORT = 12400        # порт, на котором работает сервер

# Создаём UDP-сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message = f"Hello, Server! "

# Отправляем сообщение серверу
client_socket.sendto(message.encode(), (SERVER_HOST, SERVER_PORT))  # кодируем строку в байты
print("Отправлено серверу: ", message)

# Получаем сообщение от сервера
data, addr = client_socket.recvfrom(1024)
print("Ответ от сервера: ", data.decode())

# Закрываем сокет
client_socket.close()
