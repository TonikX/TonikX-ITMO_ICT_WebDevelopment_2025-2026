import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 1234))

data = input('Введи три коэффициента (A B C) через пробел: ')
client_socket.sendall(data.encode())
print(f'Сервер обработал({client_socket.recv(1024).decode()})')
client_socket.close()