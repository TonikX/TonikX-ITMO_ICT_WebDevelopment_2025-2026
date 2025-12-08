import socket  # Импортируем модуль для работы с сетевыми сокетами

sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
# Создаём TCP-сокет (SOCK_STREAM) для IPv4 (AF_INET)

sock_client.connect(('localhost', 8080))  
# Подключаемся к серверу на localhost и порту 8080

msg = input("Enter 3 numbers (abc) separated by a space to solve the quadratic equation ax^2 + bx + c = 0\n")  
# Просим пользователя ввести 3 числа a, b и c для решения квадратного уравнения

sock_client.sendall(msg.encode())  
# Отправляем сообщение серверу, кодируя строку в байты

response = sock_client.recv(1024)  
# Получаем ответ от сервера (максимум 1024 байта)

print(f'Server: {response.decode()}')  
# Декодируем байты обратно в строку и выводим ответ сервера

sock_client.close()  
# Закрываем соединение с сервером