import socket

# Создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключаемся к серверу
client_socket.connect(('localhost', 8080))

# Отправляем сообщение серверу
a = float(input("Введите длину первого основания: "))
b = float(input("Введите длину второго основания: "))
h = float(input("Введите высоту трапеции: "))

message = f'{a}:{b}:{h}'

client_socket.sendall(message.encode())

# Получаем ответ от сервера
response = client_socket.recv(1024)
print(f'Ответ от сервера: {response.decode()}')

# Закрываем соединение
client_socket.close()
