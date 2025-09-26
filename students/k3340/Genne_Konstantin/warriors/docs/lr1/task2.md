# Задание
Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры
которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

**Требования:**

- Обязательно использовать библиотеку socket.
- Реализовать с помощью протокола TCP.
 
***

# Решение

## Клиент

```python
import socket

HOST = '127.0.0.1'
PORT = 9090

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))

print('Программа для расчёта площади трапеции')

# Пользователь вводит параметры трапеции, необходимые для подсчёта площади
while True:
    try:
        low = input('Введите длину нижнего основания: ')
        high = input('Введите длину верхнего основания: ')
        height = input('Введите длину высоты: ')
        if all(value > 0 for value in map(float, (low, high, height))):
            break
        else:
            print('Все значения должны быть положительными!')
    except:
        print('Неверный формат! Попробуйте ещё раз.')

request = f'{low} {high} {height}'

client_socket.sendall(request.encode('utf-8'))

response = client_socket.recv(1024)

print(f'Площадь трапеции: {response.decode('utf-8')}')

client_socket.close()
```

## Сервер

```python
import socket

HOST = '127.0.0.1'
PORT = 9090

def trapezoid_area(low, high, height):
    """
    Функция предназначена для подсчёта площади трапеции.
    Параметры:
        low - длина нижнего основания
        high - длина верхнего основания
        height - высота
    """
    return (low + high) / 2 * height


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen(1)

print(f'Сервер запущен на {HOST}:{PORT}')

while True:
    client_connection, client_address = server_socket.accept()

    request = client_connection.recv(1024).decode()

    response = trapezoid_area(*map(float, request.split()))

    client_connection.sendall(str(response).encode())

    client_connection.close()
```

***

# Пояснение

На сервере реализуем функцию `trapezoid_area` для подсчёта площади трапеции. Создаём TCP сокет, используя адрес `127.0.0.1` и порт `9090`, после чего в бесконечном цикле принимаем соединение и пытаемся прочитать данные от
клиента и выполнить математическую операцию. Если данные успешно получены, раскодированы и вычислен результат, то
отправляем клиенту результ и закрываем соединение с клиентом.

Клиент создает TCP сокет и пытается установить соединение с сервером на `127.0.0.1:9090`.
Далее он запрашивает данные от клиента с консоли и проводит их валидацию.
Если данные введены верно, то он отправляет их серверу, получает ответ и выводит ответ в консоль.