# Задание 2: TCP Калькулятор (Теорема Пифагора)

## Задача

Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры
которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.
Вариант: теорема Пифагора

## Реализация

Использовался протокол **TCP** (`socket.SOCK_STREAM`), который обеспечивает надежное соединение. Сервер переходит в
режим прослушивания (`listen`) и принимает входящие подключения (`accept`). Клиент устанавливает соединение с
сервером (`connect`). Данные (два катета) передавались в виде единой строки через запятую, а результат возвращался по
тому же установленному соединению.

### server.py

```python
import socket

# AF_INET - IPv4, SOCK_STREAM - TCP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcp_socket.bind(('localhost', 9999))
tcp_socket.listen(5)

while True:
    client_socket, addr = tcp_socket.accept()
    print(f"Получено соединение от {addr}")

    try:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break

        print(f"Получены данные: '{data}'")

        a_str, b_str = data.split(',')
        a = float(a_str)
        b = float(b_str)

        c = (a ** 2 + b ** 2) ** 0.5
        result = str(c)
        print(f"Вычислен результат: {result}")

        client_socket.sendall(result.encode('utf-8'))

    except ValueError:
        error_message = "Ошибка: Неверный формат данных. Ожидались два числа через запятую."
        client_socket.send(error_message.encode('utf-8'))
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        client_socket.close()
        print(f"Соединение с {addr} закрыто")

```

### client.py

```python
import socket

# AF_INET - IPv4, SOCK_STREAM - TCP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr = ('localhost', 9999)

try:
    a = input("Введите длину первого катета (a): ")
    b = input("Введите длину второго катета (b): ")

    tcp_socket.connect(addr)
    print(f"Успешно подключено")
    message = f"{a},{b}"
    tcp_socket.sendall(message.encode('utf-8'))

    result = tcp_socket.recv(1024).decode('utf-8')
    print(f"Результат от сервера: {result}")


except ConnectionRefusedError:
    print("Не удалось подключиться")
except ValueError:
    print("Ошибка ввода")
except Exception as e:
    print(f"Произошла ошибка: {e}")
finally:
    tcp_socket.close()
    print("Соединение закрыто")
```