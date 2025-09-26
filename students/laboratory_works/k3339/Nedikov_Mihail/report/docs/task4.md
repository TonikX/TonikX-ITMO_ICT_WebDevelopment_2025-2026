## Цель

Реализовать многопользовательский чат на базе **TCP-сокетов** с обработкой каждого клиента в отдельном потоке.  
Требования: использовать `socket` и для мультиклиентности — `threading`.

## Выполнение

Я сделал полноценный многопользовательский чат: один сервер принимает подключения нескольких клиентов и ретранслирует сообщения всем участникам.  
На стороне сервера я создал прослушивающий TCP‑сокет (`socket()`, `bind()`, `listen()`), а каждое входящее соединение обрабатывается в новом потоке (`threading.Thread`, функция `handle_client`).  
Чтобы безопасно хранить и обновлять список подключённых клиентов, использовал общий словарь `clients` и мьютекс `threading.Lock`. Это нужно, чтобы одновременно из разных потоков не было гонок при добавлении/удалении сокетов.

Отправка сообщений остальным участникам вынесена в функцию `broadcast`: она сначала делает «снимок» получателей под замком (чтобы список не изменился во время обхода), затем рассылает уже **без** замка (отправка может блокировать и выбрасывать исключения), а после — под замком чистит «мертвых» клиентов. Такой порядок позволяет избежать взаимоблокировок и зависаний.  
Формат обмена — JSON (функции `send_json`/`recv_json` из `utils`), это удобнее сырой строки: мы передаём тип сообщения (`join`, `chat`, `leave`, `system`) и полезные поля (`user`, `text`).

На стороне клиента TCP‑сокет соединяется с сервером (`connect()`), первым делом отправляет `join` с ником, а затем запускает отдельный поток‑слушатель `listen(...)`, который непрерывно принимает входящие сообщения (`recv_json`) и печатает их. Основной поток читает ввод пользователя и отправляет `chat`. Команда `/quit` посылает `leave`, останавливает слушателя и корректно закрывает соединение.

Таким образом, реализован настоящий многопользовательский чат с корректной работой потоков, синхронизацией доступа к общим структурам и аккуратной рассылкой сообщений.

### Сервер (TCP + threading)

```python
import socket
import threading
from utils import send_json, recv_json  # импортируем наши функции

HOST, PORT = "127.0.0.1", 9090
clients = {}
lock = threading.Lock()


def broadcast(sender_conn, obj, include_sender=False):
    # 1) берём снимок адресатов под замком
    with lock:
        targets = [c for c in clients.keys() if include_sender or c is not sender_conn]

    dead = []
    # 2) отправляем уже без замка (send может блокировать/кидать исключения)
    for c in targets:
        try:
            send_json(c, obj)
        except:
            dead.append(c)

    # 3) чистим мёртвых под замком
    if dead:
        with lock:
            for d in dead:
                if d in clients:
                    clients.pop(d, None)
                try:
                    d.close()
                except:
                    pass


def handle_client(conn, addr):
    print("Подключился:", addr)
    nick = None
    try:
        # ждём первое сообщение от клиента (должен отправить свой ник)
        hello = recv_json(conn)
        if hello and hello.get("type") == "join":
            nick = hello.get("user", f"User{addr[1]}")
            with lock:
                clients[conn] = nick
            # рассылаем системное сообщение
            broadcast(
                conn,
                {"type": "system", "text": f"*** {nick} вошёл в чат"},
                include_sender=True,
            )
        while True:
            msg = recv_json(conn)
            if msg is None:
                break
            if msg.get("type") == "leave":
                break  # клиент сам сказал, что выходит
            print(f"{nick}: {msg}")
            # пересылаем остальным как обычное сообщение
            broadcast(conn, {"type": "chat", "user": nick, "text": msg.get("text", "")})
    finally:
        left_nick = None
        with lock:
            if conn in clients:
                left_nick = clients.pop(conn)
        # ВАЖНО: broadcast — уже ВНЕ with lock
        if left_nick:
            broadcast(conn, {"type": "system", "text": f"*** {left_nick} покинул чат"})
        try:
            conn.close()
        except:
            pass


def main():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen()
    print(f"Сервер слушает {HOST}:{PORT}")

    while True:
        conn, addr = srv.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    main()
```

### Клиент (TCP + поток‑слушатель)

```python
import socket
import threading
from utils import send_json, recv_json

HOST, PORT = "127.0.0.1", 9090

running = True  # флаг для остановки потока


def listen(sock):
    global running
    while running:
        msg = recv_json(sock)
        if msg is None:
            break
        if msg["type"] == "system":
            print(msg["text"])
        elif msg["type"] == "chat":
            print(f"{msg['user']}: {msg['text']}")


def main():
    global running
    nick = input("Введите ваш ник: ")

    cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cli.connect((HOST, PORT))

    # отправляем приветственное сообщение с ником
    send_json(cli, {"type": "join", "user": nick})

    # запускаем поток-слушатель (НЕ daemon)
    listener = threading.Thread(target=listen, args=(cli,))
    listener.start()

    while True:
        text = input()
        if text.strip().lower() == "/quit":
            # отправляем уведомление серверу
            try:
                send_json(cli, {"type": "leave"})
            except:
                pass
            running = False
            break
        send_json(cli, {"type": "chat", "text": text})

    cli.close()
    listener.join()  # ждём завершения потока
    print("Вы вышли из чата.")


if __name__ == "__main__":
    main()

```

### Результат

![](assets/task4.png)

## Вывод

Реализован многопользовательский чат по TCP с потоковой обработкой клиентов и безопасной рассылкой сообщений:

сервер принимает неограниченное число подключений, каждое — в своём потоке;

клиенты одновременно отправляют и получают сообщения благодаря отдельному потоку‑слушателю;

состояние подключений защищено Lock, рассылка сделана без блокировок и с очисткой «мертвых» сокетов.
