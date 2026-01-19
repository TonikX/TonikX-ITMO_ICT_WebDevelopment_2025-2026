import socket

# Создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключаемся к серверу
client_socket.connect(('localhost', 8080))

# Получаем ответ от сервера
first_response = client_socket.recv(1024)
print(first_response.decode('utf-8'))

input_data = input('Введите данные: ')
# Отправляем сообщение серверу
client_socket.sendall(input_data.encode('utf-8'))

response = client_socket.recv(1024)

print(response.decode('utf-8'))
# Закрываем соединение
client_socket.close()