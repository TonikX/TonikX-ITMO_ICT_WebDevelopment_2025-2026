import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(('localhost', 8080))

data = input("введите 3 числа через пробел для решения уравнения вида ax^2 + bx + c = 0:\n")

client_socket.sendall(data.encode())

response = client_socket.recv(1024)
print(f'Ответ от сервера: {response.decode()}')

client_socket.close()