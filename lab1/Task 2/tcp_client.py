import socket

# Создаем UDP-сокет для отправки и получения данных
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Вводим данные параллелограмма от пользователя
a = input("Введите основание параллелограмма: ")
h = input("Введите высоту параллелограмма: ")

# Формируем сообщение в виде строки и отправляем серверу
message = f"{a} {h}"
client_socket.sendto(message.encode(), ('localhost', 8080))

# Получаем ответ от сервера и выводим его
data, server_address = client_socket.recvfrom(1024)
print(f"Ответ от сервера: {data.decode()}")

# Закрываем соединение, освобождая ресурсы
client_socket.close()
