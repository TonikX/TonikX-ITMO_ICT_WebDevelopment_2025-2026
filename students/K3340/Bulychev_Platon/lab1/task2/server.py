import socket
import math

# 2 вариант
# Решение квадратного уравнения

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen(1)
print("Server is running...")
conn, addr = server.accept()
print(f"Connected: {addr}")
data = conn.recv(1024).decode().split()
a, b, c = float(data[0]), float(data[1]), float(data[2])
d = b ** 2 - 4 * a * c
if d < 0:
    result = "No real roots"
elif d == 0:
    result = f"x = {-b / (2 * a)}"
else:
    x1 = (-b + math.sqrt(d)) / (2 * a)
    x2 = (-b - math.sqrt(d)) / (2 * a)
    result = f"x1 = {x1}, x2 = {x2}"
conn.send(result.encode())
conn.close()
server.close()
