import socket

HOST = "localhost"
PORT = 9090

# Подключаемся к серверу
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Вводим данные
a = input("Введите катет a: ")
b = input("Введите катет b: ")

# Отправляем серверу строку "a b"
message = f"{a} {b}"
client_socket.sendall(message.encode())

# Получаем ответ
response = client_socket.recv(1024).decode()
print("Ответ от сервера:", response)

client_socket.close()
