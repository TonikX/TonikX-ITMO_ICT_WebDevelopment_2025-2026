import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8080))

print(f"Решение квадратного уравнения типа ax^2 + bx + c")
a = int(input("Введите коэффициент a: "))
b = int(input("Введите коэффициент b: "))
c = int(input("Введите коэффициент c: "))

message = f"{a} {b} {c}"
client_socket.send(message.encode())

result = client_socket.recv(1024).decode()
print(f"Результат решения квадратного уравнения: {result}")

client_socket.close()