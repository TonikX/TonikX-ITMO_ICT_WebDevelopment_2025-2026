import socket

# Конфигурация сервера
Host = "127.0.0.1"  # локальный хост (localhost)
Port = 12400        # порт, на котором будет слушать сервер

# Создаём UDP-сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((Host, Port))  # привязываем сокет к IP и порту
print(f"UDP-сервер запущен на {Host}:{Port}") 

while True:
    # Получаем сообщение от клиента
    data, addr = server_socket.recvfrom(1024)  # буфер 1024 байта

    message = data.decode()  # преобразуем байты в строку
    print("Получено от", addr, ":", message)

    # Формируем и отправляем ответ клиенту
    reply = "Hello client! "
    server_socket.sendto(reply.encode(), addr)  # кодируем строку и отправляем
