# Задание 2

## Описание задачи

**Вариант 4:** Поиск площади параллелограмма
Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

## Описание решения

Было реализовано клиент-серверное приложение на Python с использованием TCP сокетов для вычисления площади параллелограмма по двум сторонам и углу между ними, с использованием библиотек socket

## Листинг кода

### server.py

```python
import socket
from math import sin, radians
from config import HOST, PORT

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.bind((HOST, PORT))
conn.listen(10)
while True:
    try:
        client_socket, addr = conn.accept()
        print(type(addr), addr)
        data = client_socket.recv(16384).decode()
        print("получен запрос:", data)

        a, b, angle = map(float, data.split(", "))
        angle = radians(angle)
        s = round(a * b * sin(angle), 2)

        client_socket.send(str(s).encode())
        client_socket.close()

    except KeyboardInterrupt:
        conn.close()
        break
```

### client.py

```python
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
```

### config.py

```python
HOST = "127.0.0.1"
PORT = 14900
```
