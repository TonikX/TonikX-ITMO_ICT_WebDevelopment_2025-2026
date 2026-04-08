import socket

SERVER_HOST = "127.0.0.1"   # адрес сервера (локальный хост)
SERVER_PORT = 12345         # порт сервера

# Создаём TCP-сокет и подключаемся к серверу
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))  # метод connect для TCP

# Просим пользователя ввести коэффициенты квадратного уравнения (ax^2 + bx + c = 0)
print("Решение квадратного уравнения ax^2 + bx + c = 0")
a = float(input("Введите коэффициент a: "))
b = float(input("Введите коэффициент b: "))
c = float(input("Введите коэффициент c: "))

# Отправляем коэффициенты a, b, c на сервер (в виде строки через запятую)
req = str(a) + "," + str(b) + "," + str(c)
client_socket.send(req.encode())  # кодируем строку в байты и отправляем

# Получаем результат от сервера
result = client_socket.recv(1024).decode()  # читаем ответ и переводим из байтов в строку

# Выводим результат на экран
print("Результат: ", result)

# Закрываем соединение
client_socket.close()
