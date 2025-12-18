# Задание 2: TCP-клиент и сервер для вычислений

## Условие

Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

*Вариант*: 1

*Операция*: Теорема Пифагора.

Требования:

- Обязательно использовать библиотеку `socket`.
- Реализовать с помощью протокола TCP.
---

## Код программы

### Сервер (server.py)

```
import socket
import math

def run_server():
    # Создаем TCP-сокет, (AF_INET - IPv4, SOCK_STREAM - TCP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('127.0.0.1', 11111))
        # Переводим сокет в режим ожидания входящих соединений
        server_socket.listen()
        print("Сервер запущен на порту 11111...")
        while True:
            # ожидаем новый сокет и адрес клиента
            client_socket, client_address = server_socket.accept()
            with client_socket:
                print(f"Подключился клиент с адресом {client_address}")
                client_message = client_socket.recv(1024).decode("UTF-8")
                try:
                    a, b = client_message.strip().split()
                    a, b = float(a), float(b)
                    c = math.hypot(a, b)
                    result = f"Гипотенуза равна {c:.4f}"
                # Ловим любые ошибки
                except Exception as e:
                    result = f"Ошибка: {e}"
                # Отправляем ответ или ошибку
                client_socket.sendall(result.encode("UTF-8"))

if __name__ == "__main__":
    run_server()
```
### Клиент (client.py)

```
import socket

def run_client():
    a = input("Введите катет 1:")
    b = input("Введите катет 2:")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(('127.0.0.1', 11111))
        # Отправляем оба катета через пробел, кодируем
        client_socket.sendall(f"{a} {b}".encode("UTF-8"))
        server_message = client_socket.recv(1024).decode("UTF-8")
        print(f"Ответ сервера: {server_message}")

if __name__ == "__main__":
    run_client()
```
## Запуск

1. Необходимо открыть два терминала.
2. В первом запустите сервер:
`py server.py`
3. Во втором терминале запустите клиент:
`py client.py`

## Результат

Cо стороны сервера: ![task2_server](assets\task2_server.jpg)

Cо стороны клиента видим: ![task2_client](assets\task2_client.jpg)

Математическая операция выполнена успешно.

## Выводы

1. Реализовано корректное TCP-взаимодействие между клиентом и сервером с использованием библиотеки `socket`.
2. Сервер обрабатывает входные данные и возвращает результат вычислений клиенту.
3. Задание выполнено в соответствии с требованиями — программа работает стабильно и обрабатывает ошибки.



