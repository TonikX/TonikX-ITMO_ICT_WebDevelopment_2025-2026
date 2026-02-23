# Задание 2

## Задание:
Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

**Операция:**

Решение квадратного уравнения.


**Требования:**

Обязательно использовать библиотеку socket.
Реализовать с помощью протокола TCP.

### Выполнение

**server_2.py**
```
    import socket
    import math

    def equation(a, b, c):
        try:
            a, b, c = float(a), float(b), float(c)
            if a == 0:
                return 'Коэффициент A не может быть равен нулю'

            discr = b ** 2 - 4 * a * c

            if discr > 0:
                x1 = (-b + math.sqrt(discr)) / (2 * a)
                x2 = (-b - math.sqrt(discr)) / (2 * a)
                return f'Ответ: X1 = {x1}, X2 = {x2}'
            elif discr == 0:
                x = -b / (2 * a)
                return f'Ответ: X = {x}'
            else:
                return 'Корней нет'

        except ValueError:
            return 'Введены некорректные числа'
```
Функция которая решает квадратное уравнение через дискриминант

```
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 1234))

    server_socket.listen(1)
    print('Сервер запущен')
```

`AF_INET` — семейство адресов IPv4;
`SOCK_STREAM` — тип сокета для TCP-соединений.
Сокет привязывается к порту 1234 на localhost.
`server_socket.listen(1)` - Сокет начинает слушать на порту 1234, принимая максимум одно соединение.

```
    while True:
        client_socket, address = server_socket.accept()
        print('Клиент подключился')


        data = client_socket.recv(1024).decode().split()
        if len(data) == 3:
            a, b, c = data
            client_socket.sendall(equation(a,b, c).encode())
        else:
            client_socket.sendall('Вы ввели не 3 значения'.encode())

        client_socket.close()
```

Бесконечный цикл, который принимает подключение от клиента. accept() блокирует выполнение программы, пока клиент не подключится.

`recv(1024)` — получает данные от клиента (максимум 1024 байта).

`decode()` — преобразует байты в строку.

`split()` — разбивает строку на список (ожидаются 3 параметра: a, b, c).

Если данных 3, вызывается функция `equation(a, b, c)`, и результат отправляется клиенту.

Если данных меньше или больше 3, клиенту отправляется сообщение об ошибке.

**client_2.py**

```
    import socket

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 1234))

    data = input('Введи три коэффициента (A B C) через пробел: ')
    client_socket.sendall(data.encode())
    print(f'Сервер обработал({client_socket.recv(1024).decode()})')
    client_socket.close()
```

Создаётся TCP-сокет `(SOCK_STREAM)`, и клиент подключается к серверу на localhost и порту 1234.

`input()` — запрашивает у пользователя ввод трёх коэффициентов A, B, C через пробел.

`encode()` — преобразует введённую строку в байты, которые отправляются серверу с помощью `sendall()`.

`recv(1024)` — получает ответ от сервера (результат решения уравнения).

`decode()` — преобразует байты в строку для отображения на экране.

#### Результаты

**Сервер**

![1](../img/task_2.1.png)

**Клиент**

![2](../img/task_2.2.png)

