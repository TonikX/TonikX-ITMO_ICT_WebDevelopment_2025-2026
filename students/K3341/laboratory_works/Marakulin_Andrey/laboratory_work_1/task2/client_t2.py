import socket
from utils import server_address

# Создаем TCP сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(server_address)

a_str = input('Введите первый катет (a): ')
b_str = input('Введите второй катет (b): ')
message = f'{a_str},{b_str}'

# Отправляем данные
client_socket.sendall(message.encode('utf-8'))

# Получаем ответ
data = client_socket.recv(1024)
print(f'Ответ сервера (гипотенуза): {data.decode("utf-8")}')

client_socket.close()
