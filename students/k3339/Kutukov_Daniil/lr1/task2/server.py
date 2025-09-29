import socket
import math

HOST = "127.0.0.1"
PORT = 12345

def pythagoras(a, b):
    return math.sqrt(a**2 + b**2)

def quadratic(a: float, b: float, c: float) -> str:
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

def trapezoid_area(a: float, b: float, h: float) -> float:
    return (a + b) * h / 2

def parallelogram_area(a: float, h: float) -> float:
    return a * h

def handle_request(request: str) -> str:
    parts = request.split()
    operation = int(parts[0])
    numbers = list(map(float, parts[1:]))

    if operation == 1:
        return f"Гипотенуза = {pythagoras(numbers[0], numbers[1])}"
    elif operation == 2:
        return quadratic(numbers[0], numbers[1], numbers[2])
    elif operation == 3:
        return f"Площадь трапеции = {trapezoid_area(numbers[0], numbers[1], numbers[2])}"
    elif operation == 4:
        return f"Площадь параллелограмма = {parallelogram_area(numbers[0], numbers[1])}"
    else:
        return "Неизвестная операция"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Сервер запущен на {HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        with conn:
            print("Подключен клиент:", addr)
            data = conn.recv(1024).decode("utf-8")
            if not data:
                break
            print("Запрос клиента:", data)
            response = handle_request(data)
            conn.sendall(response.encode("utf-8"))
