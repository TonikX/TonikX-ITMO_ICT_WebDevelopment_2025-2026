# Задача 2

## Цель
Реализовать клиентскую и серверную часть приложения с использованием библиотеки **socket** и протокола **TCP**.  
Клиент запрашивает выполнение математической операции (в данном случае — **теорема Пифагора**), сервер обрабатывает данные и возвращает результат клиенту.

## Выполнение
В ходе выполнения были реализованы клиент и сервер, где:
- **Клиент** подключается к серверу по TCP, вводит три числа и отправляет их.  
- **Сервер** принимает числа, вычисляет решение квадратного уравнения вида `ax^2 + bx + c = 0` через формулу дискриминанта и возвращает результат клиенту.  
- Также на сервере обработан случай, если уравнение не имеет действительных корней.

### Клиент
```python
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(('localhost', 8080))

data = input("введите 3 числа через пробел для решения уравнения вида ax^2 + bx + c = 0:\n")

client_socket.sendall(data.encode())

response = client_socket.recv(1024)
print(f'Ответ от сервера: {response.decode()}')

client_socket.close()
```


### Сервер
```python
import socket


def solve_sqr(a, b, c):
    d = b**2 - 4*a*c
    if d < 0:
        return "корней нет"
    else:
        return f"ответ: x1 = {(-b + d**0.5)/(2*a)}, x2 = {(-b - d**0.5)/(2*a)}"


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 8080))

server_socket.listen(1)
print("Сервер запущен на порту 8080...")

while True:
    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    request = list(map(int, client_connection.recv(1024).decode().split()))

    print(f'Данные от клиента: a:{request[0]} b:{request[1]} c:{request[2]}')

    response = solve_sqr(request[0], request[1], request[2])

    client_connection.sendall(response.encode())

    client_connection.close()
    print("соединение закрыто")
```

## Результат

Варианты ответа клиенту:

![](assets/task2client0.png)
![](assets/task2client1.png)

Работа сервера:

![](assets/task2server.png)

## Вывод

Была реализована клиент-серверная архитектура с использованием TCP-сокетов для решения квадратного уравнения.