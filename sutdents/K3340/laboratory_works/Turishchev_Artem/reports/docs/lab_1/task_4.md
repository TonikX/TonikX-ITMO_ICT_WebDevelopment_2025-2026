# Задание 4

## Описание задачи

Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте многопользовательский чат.

Реализация:

1. Протокол TCP: 100% баллов.
2. Протокол UDP: 80% баллов.
3. Для UDP используйте threading для получения сообщений на клиенте.
4. Для TCP запустите клиентские подключения и обработку сообщений от всех пользователей в потоках. Не забудьте сохранять пользователей, чтобы отправлять им сообщения.

## Описание решения

Был реализован многопользовательский чат на Python с использованием TCP сокетов и многопоточности для одновременной обработки нескольких клиентов, с использованием библиотек socket. Использовую threading для создания отдельного потока под каждого участника чата, на стороне сервера, и 2 потока которые обрабатывали исходящие и входящие сообщения на стороне клиента.

## Листинг кода

### server.py

```python
import socket
import threading
from config import HOST, PORT
from msg_dataclass import Message

clients = []

def send_message(client_socket: socket.socket, msg: Message):
    global clients
    msg = str(msg).encode()
    for client in clients:
        if client != client_socket:
            try:
                client.send(msg)
            except Exception as e:
                print(f"Error {e} while sending message to client, stoping it's connection")
                try:
                    client.close()
                except:
                    pass


def process_client(client_socket: socket.socket, addr: tuple):
    global clients

    try:
        print(f"New user with addr: {addr}")
        while True:
            msg = client_socket.recv(16384).decode()
            msg = Message.parse_msg(msg)
            if msg.type == "quit":
                break
            msg.author = addr[1]
            send_message(client_socket, msg)
    except Exception as e:
        print(f"error {e} while processing client {addr}")
    finally:
        print(f"stoping connection and thread for client {addr}")
        try:
            msg = Message(type="stop", author="server")
            client_socket.send(str(msg).encode())
            client_socket.close()
        except:
            pass
        clients.remove(client_socket)


conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.bind((HOST, PORT))
conn.listen(10)
try:
    while True:
        client_socket, addr = conn.accept()
        clients.append(client_socket)
        new_client_thread = threading.Thread(target=process_client, args=(client_socket, addr), daemon=True)
        new_client_thread.start()
except Exception as e:
    print(f"Error {e} while server running, trying to send messages of stop, and shutting down")
    try:
        msg = Message(type="stop", author="server")
        send_message(conn, msg)
    except:
        print("err")
finally: 
    conn.close()
```

### client.py

```python
import socket
import threading
from config import HOST, PORT
from msg_dataclass import Message


def reciever(conn: socket.socket, stop: threading.Event):
    while not stop.is_set():
        try:
            msg = conn.recv(16384).decode()
            msg = Message.parse_msg(msg)
            if msg.type == "stop" and msg.author == "server":
                stop.set()
                print(f"recieved stop message from server")
                break
            else:
                print(f"{msg.author}: {msg.msg}")
        except Exception as e:
            print(f"error {e} while recieving")
            stop.set()

def sender(conn: socket.socket, stop: threading.Event):
    try:
        while not stop.is_set():
            msg = input()
            if msg == "exit":
                stop.set()
                print("Exit command recieved")
                break
            msg = Message(msg=msg)
            conn.send(str(msg).encode())
    except Exception as e:
        print(f"error {e} during sending msg")
        stop.set()

print('Type messages to send, type "exit" to stop client')
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((HOST, PORT))
stop = threading.Event()
reciever_thread = threading.Thread(target=reciever, args=(conn, stop), daemon=True)
sender_thread = threading.Thread(target=sender, args=(conn, stop), daemon=True)

reciever_thread.start()
sender_thread.start()
try:
    while not stop.is_set():
        stop.wait(timeout=0.5)
except Exception as e:
    print(f"Error {e} in client")
finally:
    try:
        msg = Message(type="quit")
        conn.send(str(msg).encode())
    except:
        pass
    print("shutting down client")
    try:
        conn.close()
    except:
        pass
```

### msg_dataclass.py

```python
import json
from dataclasses import dataclass, asdict

@dataclass
class Message:
    type: str = ""
    msg: str = ""
    author: str = "self"

    def __str__(self):
        return json.dumps(asdict(self))
    
    @classmethod
    def parse_msg(cls, msg):
        msg = json.loads(msg)
        return cls(**msg)
```

### config.py

```python
HOST = "127.0.0.1"
PORT = 14900
```
