import socket

# Создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4, TCP

# Подключаемся к серверу
client_socket.connect(('localhost', 8080))

# Получаем данные от пользователя
print("Введите параметры трапеции:")
base1 = input("Первое основание: ")
base2 = input("Второе основание: ")
height = input("Высота: ")

# Формируем и отправляем сообщение серверу
message = base1 + ',' + base2 + ',' + height
client_socket.sendall(message.encode())

# Получаем ответ от сервера
response = client_socket.recv(1024).decode()
print(f'Ответ от сервера: {response}')

# Закрываем соединение
client_socket.close()