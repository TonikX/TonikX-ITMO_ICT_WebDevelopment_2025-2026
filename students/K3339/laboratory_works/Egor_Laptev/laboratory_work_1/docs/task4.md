## Задание 4:
Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте многопользовательский чат.

### Используемые технологии:
- Python `socket`
- Python `threading`
- Протокол TCP

### Файлы:

**client.py**
```python
import socket
import threading

HOST = 'localhost'
PORT = 8080


def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            print(message)
        except:
            print("Вы отключены от сервера.")
            sock.close()
            break


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    print(sock.recv(1024).decode())
    nickname = input("Ваше имя: ")
    sock.send(nickname.encode())

    thread = threading.Thread(target=receive_messages, args=(sock,))
    thread.start()

    while True:
        message = input()
        if message.lower() == 'exit':
            sock.close()
            break
        sock.send(f"{nickname}: {message}".encode())


if __name__ == "__main__":
    main()

```

**server.py**
```python
import socket
import threading

HOST = 'localhost'
PORT = 8080

clients = []
nicknames = []


def broadcast(message, _client=None):
    for client in clients:
        if client != _client:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)


def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                break
            broadcast(message, client)
        except:
            clients.remove(client)
            client.close()
            break


def receive_connections():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen()
    print(f"Сервер запущен на {HOST}:{PORT}")

    while True:
        client, addr = sock.accept()
        print(f"Подключился {addr}")
        client.send("Введите ваше имя: ".encode())
        nickname = client.recv(1024).decode()
        nicknames.append(nickname)
        clients.append(client)
        print(f"Пользователь {nickname} присоединился.")
        broadcast(f"{nickname} присоединился в чат.".encode(), client)

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    receive_connections()
```

### Результат работы:
Сервер:
```
Сервер запущен на localhost:8080
Подключился ('127.0.0.1', 53215)
Пользователь Alice присоединился.
Подключился ('127.0.0.1', 53216)
Пользователь Bob присоединился.

```
Клиент выводит на консоль:

```
Введите ваше имя: Alice
Bob присоединился в чат.
Привет, Bob!
Bob: Привет, Alice!
```