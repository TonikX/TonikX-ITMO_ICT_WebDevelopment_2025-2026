import socket

# TCP-клиент устанавливает соединение и передает пару чисел.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключаемся к серверу на указанном порту.
client_socket.connect(("localhost", 8080))

data = input("Введите два числа через пробел (например, 3 4): ")

# Отправляем введенные данные на сервер.
client_socket.sendall(data.encode())

# Получаем строку-ответ с результатом и показываем ее пользователю.
response = client_socket.recv(1024)
print(response.decode())

# Закрываем соединение.
client_socket.close()
