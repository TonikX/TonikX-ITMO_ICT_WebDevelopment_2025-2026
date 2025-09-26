# Задача 2

## Цель
Реализовать клиентскую и серверную часть приложения с использованием библиотеки **socket** и протокола **TCP**.  
Клиент запрашивает выполнение математической операции (в данном случае — **теорема Пифагора**), сервер обрабатывает данные и возвращает результат клиенту.

## Выполнение
В данной задаче реализована программа, где:
- **Клиент** подключается к серверу по TCP, вводит два числа и отправляет их.  
- **Сервер** принимает числа, вычисляет гипотенузу по теореме Пифагора `sqrt(a^2 + b^2)` и возвращает результат клиенту.  
- Обработаны ошибки: если введено меньше/больше чисел или отрицательные значения.

### Клиент
```python
import socket

# Создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключаемся к серверу
client_socket.connect(("localhost", 8080))

data = input("Введите два числа через пробел (Теорема Пифагора): ")

# Отправляем сообщение серверу
client_socket.sendall(data.encode())

# Получаем ответ от сервера
response = client_socket.recv(1024)
print(response.decode())

# Закрываем соединение
client_socket.close()
```


### Сервер
```python
import socket
import math

# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к адресу и порту
server_socket.bind(("localhost", 8080))

# Начинаем слушать входящие подключения (ожидание клиентов)
server_socket.listen(1)

while True:
    # Принимаем соединение от клиента
    client_connection, client_address = server_socket.accept()

    # Получаем сообщение от клиента
    request = client_connection.recv(1024).decode()

    try:
        numbers = list(map(float, request.split()))
        if len(numbers) != 2:
            raise ValueError("Нужно ввести ровно два числа.")
        if any(n < 0 for n in numbers):
            raise ValueError("Числа должны быть неотрицательными.")
        result = str(math.sqrt(numbers[0] ** 2 + numbers[1] ** 2))
    except ValueError:
        result = "Ошибка: Введите два неотрицательных числа через пробел."

    # Отправляем ответ клиенту
    client_connection.sendall(result.encode())

    # Закрываем соединение
    client_connection.close()
```

## Результат

Пример работы программы:

![](assets/task2.png)

## Вывод

Была реализована клиент-серверная архитектура с использованием TCP-сокетов.
Клиент передает два числа, сервер рассчитывает гипотенузу по теореме Пифагора и возвращает результат.