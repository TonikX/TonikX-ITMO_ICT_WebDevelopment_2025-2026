# Задание
Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте 
многопользовательский чат.

**Требования:**

- Обязательно использовать библиотеку socket.
- Для многопользовательского чата необходимо использовать библиотеку threading.
- Протокол TCP: 100% баллов.
- Протокол UDP: 80% баллов.
- Для UDP используйте threading для получения сообщений на клиенте.
- Для TCP запустите клиентские подключения и обработку сообщений от всех пользователей в потоках. Не забудьте сохранять
пользователей, чтобы отправлять им сообщения.
 
***

# Решение

## Клиент

```python
import socket
import threading

HOST = '127.0.0.1'
PORT = 9090

nickname = input("Введите имя: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


def receive_message():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'nickname':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("Ошибка получения сообщения.")
            client.close()
            break


def write_message():
    while True:
        message = f"{nickname}: {input('')}"
        client.send(message.encode('utf-8'))


receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

write_thread = threading.Thread(target=write_message)
write_thread.start()


```

## Сервер

```python
import socket
import threading

HOST = '127.0.0.1'
PORT = 9090

clients = []    # общий список клиентов
nicknames = []  # общий список никнеймов


def broadcast(message):
    for client in clients:
        client.send(message)


def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f"{nickname} покинул чат.".encode('utf-8'))
            break


def main():
    sock = socket.socket()
    sock.bind((HOST, PORT))
    sock.listen(5)

    print(f"Сервер запущен {HOST, PORT}")

    while True:
        client, address = sock.accept()
        print(f"Подключен {address}")

        client.send('nickname'.encode('utf-8'))  # запрос никнейма
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Имя клиента: {nickname}")
        broadcast(f"{nickname} подключился к чату!".encode('utf-8'))
        client.send("Вы подключены к чату!".encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    main()

```

***

# Пояснение

# Простой чат-сервер на Python

Данный код реализует многопользовательский чат-сервер, работающий по локальной сети.

## Принцип работы

1. Сервер запускается и ожидает подключения клиентов
2. При подключении новый клиент получает запрос на ввод ника
3. Сервер сохраняет клиента и его ник в общие списки
4. Все сообщения от одного клиента автоматически рассылаются всем остальным
5. При отключении клиента остальные участники получают уведомление

## Основные компоненты

- **`broadcast(message)`** — отправляет полученное сообщение всем подключённым клиентам
- **`handle_client(client)`** — обрабатывает сообщения конкретного клиента в отдельном потоке
- **`main()`** — главный цикл сервера, принимает новые подключения и создаёт потоки

## Особенности реализации

- Каждый клиент работает в отдельном потоке (`threading`)
- Сервер может обслуживать несколько клиентов одновременно
- Используется сокет TCP (`socket.SOCK_STREAM`)
- При отключении клиента автоматически удаляет его из списков и оповещает других

## Технические детали

- **Хост:** `127.0.0.1` (локальный)
- **Порт:** `9090`
- **Максимальная очередь подключений:** 5
- **Размер буфера:** 1024 байта