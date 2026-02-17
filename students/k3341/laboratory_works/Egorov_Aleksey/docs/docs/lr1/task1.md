# Задание
Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно
отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно
отобразиться у клиента.

**Требования:**

 - Обязательно использовать библиотеку socket.
 - Реализовать с помощью протокола UDP.
 
***

# Решение

## Клиент

```python
import socket

HOST = '127.0.0.1'
PORT = 9090


def main():
    # Создаём сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Отправляем сообщения
    message = 'Hello, server'
    client_socket.sendto(message.encode('utf-8'), (HOST, PORT))

    # Получаем ответа
    try:
        server_data, server_address = client_socket.recvfrom(1024)
        print(f"Ответ от сервера: {server_data.decode('utf-8')}")
    except:
        print("Сервер недоступен.")

    # Закрываем сокет
    client_socket.close()


if __name__ == '__main__':
    main()

```

## Сервер

```python
import socket

HOST = '127.0.0.1'
PORT = 9090


def main():
    # Создаем сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Привязываем сокет к адресу и порту
    server_socket.bind((HOST, PORT))

    print(f"Сервер запущен на {HOST}:{PORT}")

    while True:
        # Получаем данные от клиента и его адрес
        client_data, client_address = server_socket.recvfrom(1024)
        print(f"Сообщение от клиента: {client_data.decode('utf-8')}")

        # Отправляем ответ клиенту
        message = 'Hello, client'
        server_socket.sendto(message.encode('utf-8'), client_address)


if __name__ == '__main__':
    main()

```

***

# Пояснение

Создаём UDP сокет на сервере, используя адрес `127.0.0.1` и порт `9090`, после чего в бесконечном цикле пытаемся прочитать данные от
клиента и напечатать их, а затем отправить сообщение `Hello, client` клиенту.

Клиент создает UDP сокет и без установки соединения отправляет данные на `127.0.0.1:9090`. Затем читает ответ от сервера и закрывает сокет.
