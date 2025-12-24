# TCP чат с поддержкой нескольких клиентов

## Условие задания  
Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте многопользовательский чат.

**Требования:**  
- Использовать библиотеку `socket`. 
- Для многопользовательского чата необходимо использовать библиотеку `threading`.

## Алгоритм решения  
- Сервер создаёт TCP-сокет и привязывает его к адресу и порту, затем переходит в режим прослушивания подключений (`listen`).  
- Сервер использует список для хранения активных клиентов и блокировку (`threading.Lock`) для безопасного доступа к списку в потоках.  
- При подключении нового клиента сервер добавляет его сокет в список и создаёт отдельный поток для обработки сообщений этого клиента.  
- Поток сервера принимает сообщения от клиента (`recv`) и пересылает их всем остальным подключённым клиентам.  
- Если клиент отключается или соединение разрывается, сервер удаляет его из списка активных клиентов и закрывает сокет.  
- Клиент создаёт TCP-сокет и подключается к серверу.  
- Клиент запускает отдельный поток для приёма сообщений от сервера, чтобы не блокировать ввод пользователя.  
- Клиент вводит сообщения и отправляет их на сервер; при вводе команды `exit` клиент закрывает соединение.  
- Сервер и клиент работают в бесконечных циклах, позволяя многопользовательскую коммуникацию в реальном времени.

## Код сервера
```python
import socket
import threading

clients = []
clients_lock = threading.Lock()


def handle_client(client_socket, address):
    
    print(f"[+] Подключился новый клиент: {address}")

    try:
        while True:
    
            message = client_socket.recv(1024).decode('utf-8')

            if not message:
                break

            print(f"Сообщение от {address}: {message}")

            message_to_send = f"[{address}] {message}"

            with clients_lock:
                for client in clients[:]:
                    if client != client_socket:
                        try:
                            client.send(message_to_send.encode('utf-8'))
                        except:
                            clients.remove(client)
    except (ConnectionResetError, BrokenPipeError):
        print(f"[-] Соединение с клиентом {address} было разорвано.")
    finally:
        with clients_lock:
            if client_socket in clients:
                clients.remove(client_socket)
                print(f"[-] Клиент {address} отключен. Активных клиентов: {len(clients)}")
        client_socket.close()


def start_server(host='localhost', port=12345):
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((host, port))

    server_socket.listen(5)
    print(f"[*] Сервер запущен на {host}:{port}. Ожидание подключений...")

    try:
        while True:
            client_socket, address = server_socket.accept()

            with clients_lock:
                clients.append(client_socket)
                print(f"[*] Активных клиентов: {len(clients)}")

            client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
            client_thread.daemon = True
            client_thread.start()

    except KeyboardInterrupt:
        print("\n[*] Остановка сервера...")
    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()
```

## Код клиента
```python
import socket
import threading


def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if message:
                print(f"\n{message}\nВаше сообщение: ", end="")
            else:
                print("\n[*] Соединение с сервером разорвано.")
                break
        except (ConnectionResetError, BrokenPipeError):
            print("\n[*] Потеряно соединение с сервером.")
            break
        except OSError:
            break


def start_client(host='localhost', port=12345):

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))
        print(f"[*] Подключено к серверу {host}:{port}")
        print("[*] Для выхода введите 'exit'")

        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.daemon = True
        receive_thread.start()

        while True:
            message = input("Ваше сообщение: ")
            if message.lower() == 'exit':
                print("[*] Отключение от сервера...")
                break
            client_socket.send(message.encode('utf-8'))

    except ConnectionRefusedError:
        print(f"[-] Не удалось подключиться к серверу {host}:{port}")
    except KeyboardInterrupt:
        print("\n[*] Принудительное отключение...")
    finally:
        client_socket.close()


if __name__ == "__main__":
    start_client()
```

## Результат работы
```python
Сервер
[*] Сервер запущен на localhost:12345. Ожидание подключений...
[*] Активных клиентов: 1
[+] Подключился новый клиент: ('127.0.0.1', 56676)
Сообщение от ('127.0.0.1', 56676): Hi!
[*] Активных клиентов: 2
[+] Подключился новый клиент: ('127.0.0.1', 56685)
[*] Активных клиентов: 3
[+] Подключился новый клиент: ('127.0.0.1', 56691)
Сообщение от ('127.0.0.1', 56676): Hi!
Сообщение от ('127.0.0.1', 56685): Hello!
[-] Соединение с клиентом ('127.0.0.1', 56676) было разорвано.
[-] Клиент ('127.0.0.1', 56676) отключен. Активных клиентов: 2

Клиент №1
[*] Подключено к серверу localhost:12345
[*] Для выхода введите 'exit'
Ваше сообщение: Hi!
Ваше сообщение:
[('127.0.0.1', 56685)] Hello!

Клиент №2
[*] Подключено к серверу localhost:12345
[*] Для выхода введите 'exit'
Ваше сообщение: 
[('127.0.0.1', 56676)] Hi!
Ваше сообщение: Hello!
Ваше сообщение: exit
[*] Отключение от сервера...

Клиент №3
[*] Подключено к серверу localhost:12345
[*] Для выхода введите 'exit'
Ваше сообщение: 
[('127.0.0.1', 56676)] Hi!
Ваше сообщение:
[('127.0.0.1', 56685)] Hello!

```