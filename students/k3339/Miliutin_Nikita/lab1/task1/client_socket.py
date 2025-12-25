import socket

# Создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

data = 'Привет, сервер!'
# Подключаемся к серверу
client_socket.sendto(data.encode("utf-8"), ('localhost', 9090))


# Получаем ответ от сервера 
data, addr = client_socket.recvfrom(1024)

print(f'Ответ от сервера: {data.decode()} (вывел клиент)')

