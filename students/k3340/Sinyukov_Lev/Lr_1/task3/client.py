import socket

# Создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключаемся к серверу
client_socket.connect(('localhost', 8080))

# Получаем ответ от сервера
response =  b""
while True:
    part_response = client_socket.recv(1024)
    if not part_response:
        break
    response += part_response

print(f'Ответ от сервера: {response.decode()}')
# Закрываем соединение
client_socket.close()