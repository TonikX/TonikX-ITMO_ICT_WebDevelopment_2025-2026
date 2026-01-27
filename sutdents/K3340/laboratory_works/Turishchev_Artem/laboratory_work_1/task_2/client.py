import socket
from config import HOST, PORT

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((HOST, PORT))
a = input("Введите первую сторону(нецулые числа через точку например: 1.5)): ")
b = input("Введите вторую сторону: ")
angle = input("Введите угол в градусах: ")
msg = ", ".join([a, b, angle])
conn.send(msg.encode())
response = conn.recv(16384).decode()
conn.close()
print(f"Получившаяся площадь: {response}")
