import socket

# Создаем TCP сокет
# AF_INET - используем IPv4
# SOCK_STREAM - указываем TCP протокол
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Устанавливаем соединение с сервером
client.connect(('localhost', 8080))

# Отправляем HTTP GET-запрос
client.send(b"GET / HTTP/1.1\r\n\r\n")

# Получаем ответ от сервера
response = client.recv(4096).decode('utf-8')

# Выводим ответ
print(response)

# Закрываем соединение
client.close()