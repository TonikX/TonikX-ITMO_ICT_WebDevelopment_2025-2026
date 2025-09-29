# Отчет по заданию 4: Многопользовательский чат

## Цель работы
Реализовать многопользовательский чат с использованием протокола TCP и потоков для обработки одновременных подключений нескольких клиентов.

## Код программы

### server.py
```python
import socket
import threading

HOST = "127.0.0.1"
PORT = 50000

clients_lock = threading.Lock()
clients = {}

def broadcast(message: str, exclude_sock=None):
    with clients_lock:
        to_remove = []
        for sock in list(clients.keys()):
            if sock is exclude_sock:
                continue
            try:
                sock.sendall(message.encode("utf-8"))
            except Exception:
                to_remove.append(sock)
        for s in to_remove:
            remove_client(s)

def remove_client(sock):
    with clients_lock:
        name = clients.pop(sock, None)
    try:
        sock.close()
    except:
        pass
    if name:
        print(f"[DISCONNECTED] {name}")
        broadcast(f"*** {name} отключился(ась) ***\n")

def handle_client(conn, addr):
    try:
        name = conn.recv(1024).decode("utf-8").strip()
        if not name:
            conn.close()
            return
        with clients_lock:
            clients[conn] = name
        print(f"[CONNECTED] {name} from {addr}")
        broadcast(f"*** {name} подключился(ась) ***\n", exclude_sock=conn)
        conn.sendall("Добро пожаловать в чат! Введите сообщение, или /quit для выхода.\n".encode("utf-8"))

        while True:
            data = conn.recv(4096)
            if not data:
                break
            text = data.decode("utf-8").strip()
            if text == "/quit":
                break
            message = f"{name}: {text}\n"
            print(message.strip())
            broadcast(message, exclude_sock=conn)
    except Exception as e:
        print("Ошибка с клиентом:", e)
    finally:
        remove_client(conn)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen()
        print(f"TCP чат-сервер запущен на {HOST}:{PORT}")
        try:
            while True:
                conn, addr = srv.accept()
                thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
                thread.start()
        except KeyboardInterrupt:
            print("Сервер завершается...")
            with clients_lock:
                for s in list(clients.keys()):
                    try:
                        s.sendall("Сервер закрывается.\n".encode("utf-8"))
                        s.close()
                    except:
                        pass

if __name__ == "__main__":
    main()
```

### client.py
```python
import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 50000

def receive_loop(sock):
    try:
        while True:
            data = sock.recv(4096)
            if not data:
                print("Соединение закрыто сервером.")
                break
            print(data.decode("utf-8"), end="")
    except Exception as e:
        print("Ошибка при получении:", e)
    finally:
        try:
            sock.close()
        except:
            pass
        sys.exit(0)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        t = threading.Thread(target=receive_loop, args=(sock,), daemon=True)
        t.start()

        try:
            while True:
                line = input()
                if line.strip() == "":
                    continue
                sock.sendall(line.encode("utf-8"))
                if line == "/quit":
                    break
        except (KeyboardInterrupt, EOFError):
            sock.sendall("/quit".encode("utf-8"))

if __name__ == "__main__":
    main()
```

## Описание работы программы
### Серверная часть
* Многопоточная архитектура: Каждое клиентское подключение обрабатывается в отдельном потоке
* Управление клиентами: Используется словарь clients для хранения подключенных пользователей
* Синхронизация: Применяется threading.Lock() для безопасного доступа к общим ресурсам
* Функциональность:
* * Регистрация пользователей по имени
* * Широковещательная рассылка сообщений всем клиентам
* * Обработка отключений клиентов
* * Команда /quit для выхода из чата

### Клиентская часть:
* Двухпоточная архитектура:

* * Главный поток: отправка сообщений

* * Дочерний поток: прием сообщений от сервера

* Неблокирующий ввод: Пользователь может печатать сообщения, одновременно получая сообщения от других участников