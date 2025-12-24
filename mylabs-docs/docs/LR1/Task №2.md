# Реализация клиентской и серверной части приложения (TCP)

## Условие задания  
Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции (квадратное уравнение), параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту. 

**Требования:**  
- Использовать библиотеку `socket`.  
- Реализовать через протокол TCP.  

## Алгоритм решения  
- Сервер создаёт TCP-сокет и привязывает его к адресу `('localhost', 8080)`.  
- Сервер переходит в режим прослушивания входящих подключений (`listen`).  
- Клиент создаёт TCP-сокет и подключается к серверу.  
- Клиент запрашивает у пользователя ввод коэффициентов `a`, `b` и `c`.  
- Клиент формирует сообщение в формате `"a,b,c"` и отправляет серверу (`sendall`).  
- Сервер принимает данные от клиента (`recv`) и парсит значения `a`, `b`, `c`.  
- Сервер вычисляет дискриминант `D = b^2 - 4*a*c` для решения квадратного уравнения:
  - Если `D > 0`: вычисляет два корня и формирует результат.  
  - Если `D == 0`: вычисляет один корень.  
  - Если `D < 0`: сообщает, что действительных корней нет.  
- Сервер отправляет результат клиенту (`sendall`).  
- Сервер закрывает соединение с клиентом, клиент получает ответ и выводит его на экран. 

## Код сервера
```python
import socket
import math

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 8080))

server_socket.listen(1)

while True:
    client_connection, client_address = server_socket.accept()

    data = client_connection.recv(1024).decode()

    a_str, b_str, c_str = data.split(',')
    a, b, c = float(a_str), float(b_str), float(c_str)

    D = b**2 - 4*a*c
    if D > 0:
        x1 = (-b + math.sqrt(D)) / (2*a)
        x2 = (-b - math.sqrt(D)) / (2*a)
        result = f"Два корня: x1 = {x1}, x2 = {x2}"
    elif D == 0:
        x = -b / (2*a)
        result = f"Один корень: x = {x}"
    else:
        result = "Действительных корней нет"

    client_connection.sendall(result.encode())

    client_connection.close()
```

## Код клиента
```python
import socket

a = input("Введите коэффициент a: ")
b = input("Введите коэффициент b: ")
c = input("Введите коэффициент c: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(('localhost', 8080))

message = f"{a},{b},{c}"
client_socket.sendall(message.encode())

response = client_socket.recv(1024)
print(f"Ответ от сервера: {response.decode()}")

client_socket.close()
```

## Результат работы
```python
Введите коэффициент a: 1
Введите коэффициент b: -3
Введите коэффициент c: 2
Ответ от сервера: Два корня: x1 = 2.0, x2 = 1.0
```