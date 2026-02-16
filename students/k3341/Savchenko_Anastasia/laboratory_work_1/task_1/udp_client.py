import socket

# Создаем UDP сокет
# AF_INET - используем IPv4
# SOCK_DGRAM - указываем UDP протокол
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Отправляем сообщение серверу
# sendto принимает (данные, (адрес, порт))
client.sendto("Hello, server".encode('utf-8'), ('localhost', 1234))

# Получаем ответ от сервера
# recvfrom возвращает (данные, адрес_сервера)
print(client.recvfrom(1024)[0].decode('utf-8'))

# Закрываем соединение
client.close()