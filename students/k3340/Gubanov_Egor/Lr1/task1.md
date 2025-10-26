# Задание 1: UDP-клиент и сервер

## Практическое задание

Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

### Требования:
- Обязательно использовать библиотеку `socket`
- Реализовать с помощью протокола **UDP**

### Полезные ссылки:
- [Habr: Основы работы с сокетами](https://habr.com/ru/articles/340682/)
- [Андрей Малинин: Сокеты в Python](https://python-scripts.com/sockets)
- [Документация Python: Руководство по сокетам](https://docs.python.org/3/howto/sockets.html)
- [Python Library Reference: socket](https://docs.python.org/3/library/socket.html)
- [Видео: Введение в работу с сокетами](https://www.youtube.com/watch?v=3QiLXLh0Q1s)

---

## Реализация

### Сервер (task1/server.py)

```python
import socket

HOST = '127.0.0.1'
PORT = 8001
BUFFER_SIZE = 1024
ENCODING = 'utf-8'

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        print(f"UDP сервер запущен на {HOST}:{PORT}")
        try:
            while True:
                data, addr = s.recvfrom(BUFFER_SIZE)
                if not data:
                    continue
                msg = data.decode(ENCODING)
                print(f"Получено от {addr}: {msg!r}")
                reply = "Hello, client" if msg.strip() == "Hello, server" else f"Server received: {msg}"
                s.sendto(reply.encode(ENCODING), addr)
        except KeyboardInterrupt:
            print("\nСервер завершает работу.")

if __name__ == '__main__':
    main()
```

### Клиент (task1/client.py)

```python
import socket

HOST = '127.0.0.1'
PORT = 8001
ENCODING = 'utf-8'
TIMEOUT = 5.0

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(TIMEOUT)
        s.sendto("Hello, server".encode(ENCODING), (HOST, PORT))
        try:
            data, _ = s.recvfrom(1024)
            print("Сервер:", data.decode(ENCODING))
        except socket.timeout:
            print("Нет ответа")

if __name__ == '__main__':
    main()
```

## Запуск

1. Откройте два терминала
2. В первом запустите сервер:
   ```bash
   python task1/server.py
   ```
3. Во втором запустите клиент:
   ```bash
   python task1/client.py
   ```

## Результат

**Сервер:**
```
UDP сервер запущен на 127.0.0.1:8001
Получено от ('127.0.0.1', 54321): 'Hello, server'
```

**Клиент:**
```
Сервер: Hello, client
```

## Выводы

1. Реализовано простое взаимодействие между клиентом и сервером через UDP-соединение
2. Сообщения корректно передаются и отображаются с обеих сторон
3. Использован минимальный, но достаточный набор функций библиотеки `socket`
4. UDP не гарантирует доставку пакетов, но в локальной сети работает надежно
