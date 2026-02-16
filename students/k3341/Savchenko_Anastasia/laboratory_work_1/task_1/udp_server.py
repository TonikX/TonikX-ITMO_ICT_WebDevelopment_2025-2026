import socket

# Создаем UDP сокет
# AF_INET - используем IPv4
# SOCK_DGRAM - указываем UDP протокол
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # SOCK_DGRAM --> UDP протокол

# Привязываем сокет к адресу и порту
server.bind(('localhost', 1234))

# Получаем сообщение от клиента
# recvfrom возвращает (данные, адрес_клиента)
message_client, address_client = server.recvfrom(1024)

# Декодируем и выводим сообщение
print(message_client.decode('utf-8'))

# Отправляем ответ клиенту
server.sendto("Hello, client".encode('utf-8'), address_client)

# Закрываем соединение
server.close()