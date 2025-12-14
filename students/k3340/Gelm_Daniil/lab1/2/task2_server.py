import socket
import math

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8889))
server_socket.listen(5)

print("Сервер запущен на порту 8889")

def pythagorean(a, b):
    return math.sqrt(a * a + b * b)

while True:
    client_socket, addr = server_socket.accept()
    print(f"Подключен клиент: {addr}")
    
    data = client_socket.recv(1024).decode('utf-8')
    try:
        a, b = map(float, data.split(','))
        result = pythagorean(a, b)
        response = str(result)
    except:
        response = "Ошибка: некорректные данные"
    
    client_socket.send(response.encode('utf-8'))
    client_socket.close()

