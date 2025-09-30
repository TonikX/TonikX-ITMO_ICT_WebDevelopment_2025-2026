import socket
import math

HOST = "127.0.0.1"
PORT = 12345

def pythagoras(a, b):
    return math.sqrt(a**2 + b**2)

def quadratic(a, b, c):
    d = b**2 - 4*a*c
    if d < 0:
        return "Нет действительных корней"
    elif d == 0:
        x = -b / (2*a)
        return f"Один корень: x = {x}"
    else:
        x1 = (-b + math.sqrt(d)) / (2*a)
        x2 = (-b - math.sqrt(d)) / (2*a)
        return f"Два корня: x1 = {x1}, x2 = {x2}"

def trapezoid(a, b, h):
    return 0.5 * (a + b) * h

def parallelogram(a, h):
    return a * h

# Создаём TCP-сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Сервер TCP запущен на {HOST}:{PORT} и ожидает подключения...")

while True:
    conn, addr = server_socket.accept()
    print(f"Подключился клиент: {addr}")

    data = conn.recv(1024).decode()
    if not data:
        conn.close()
        continue

    # Разбираем данные от клиента
    parts = data.split()
    operation = int(parts[0])   # номер операции
    params = list(map(float, parts[1:]))

    # Выполняем нужную операцию
    if operation == 1:
        result = f"Гипотенуза = {pythagoras(params[0], params[1])}"
    elif operation == 2:
        result = quadratic(params[0], params[1], params[2])
    elif operation == 3:
        result = f"Площадь трапеции = {trapezoid(params[0], params[1], params[2])}"
    elif operation == 4:
        result = f"Площадь параллелограмма = {parallelogram(params[0], params[1])}"
    else:
        result = "Неизвестная операция"

    # Отправляем результат клиенту
    conn.send(result.encode())
    conn.close()
