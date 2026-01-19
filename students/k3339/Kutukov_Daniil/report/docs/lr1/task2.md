# Задание 2: TCP клиент-серверное приложение для математических операций

## Цель работы
Реализовать клиентскую и серверную часть приложения с использованием протокола TCP, где клиент запрашивает выполнение математических операций, а сервер обрабатывает запросы и возвращает результаты.

## Код программы

### server.py
```python
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
```

### client.py
```python
import socket

HOST = "127.0.0.1"
PORT = 12345

menu = """
Выберите операцию:
1 - Теорема Пифагора (a, b)
2 - Квадратное уравнение (a, b, c)
3 - Площадь трапеции (a, b, h)
4 - Площадь параллелограмма (a, h)
"""

print(menu)
choice = int(input("Введите номер операции: "))

if choice == 1:
    a = float(input("Введите a: "))
    b = float(input("Введите b: "))
    request = f"{choice} {a} {b}"
elif choice == 2:
    a = float(input("Введите a: "))
    b = float(input("Введите b: "))
    c = float(input("Введите c: "))
    request = f"{choice} {a} {b} {c}"
elif choice == 3:
    a = float(input("Введите основание a: "))
    b = float(input("Введите основание b: "))
    h = float(input("Введите высоту h: "))
    request = f"{choice} {a} {b} {h}"
elif choice == 4:
    a = float(input("Введите сторону a: "))
    h = float(input("Введите высоту h: "))
    request = f"{choice} {a} {h}"
else:
    print("Неверный выбор")
    exit()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    client_socket.sendall(request.encode("utf-8"))
    data = client_socket.recv(1024).decode("utf-8")

print("Результат:", data)
```

## Описание работы программы

### Серверная часть
- Создает TCP-сокет с помощью `socket.socket(socket.AF_INET, socket.SOCK_STREAM)`
- Привязывает сокет к локальному адресу и порту с помощью `bind()`
- Ожидает подключения клиентов с помощью `listen()`
- Реализует 4 математические операции:
  - Теорема Пифагора
  - Решение квадратного уравнения
  - Площадь трапеции
  - Площадь параллелограмма
- Обрабатывает запросы клиентов и возвращает результаты

### Клиентская часть
- Создает TCP-сокет и подключается к серверу
- Предоставляет пользователю меню для выбора операции
- Запрашивает необходимые параметры для выбранной операции
- Отправляет запрос на сервер и получает результат