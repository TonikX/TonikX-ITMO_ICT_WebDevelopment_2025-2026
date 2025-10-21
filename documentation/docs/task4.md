# Задание 4

Реализовать **многопользовательский чат**. Запуск нескольких экземпляров `client.py` подключает несколько пользователей.

**Требования:**
- Использовать библиотеку `socket`.
- Для многопользовательского чата использовать `threading`.
- Протокол **TCP**.

---

## Решение

### Сервер 
```python
import socket
import threading

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9092

connected_clients = []
connected_clients_lock = threading.Lock()

def broadcast_message(text_message):
    with connected_clients_lock:
        for client in connected_clients:
            try:
                client["socket"].sendall((text_message + "\n").encode("utf-8"))
            except Exception:
                pass

def handle_client_connection(client_socket, client_address):
    client_file = client_socket.makefile("r", encoding="utf-8", newline="\n")
    try:
        user_name = client_file.readline()
        if not user_name:
            client_socket.close()
            return
        user_name = user_name.strip()

        with connected_clients_lock:
            connected_clients.append({"socket": client_socket, "file": client_file, "name": user_name})

        print(f"Подключился пользователь: {user_name} {client_address}")
        broadcast_message(f"[СИСТЕМА] Пользователь {user_name} вошёл в чат.")

        while True:
            line = client_file.readline()
            if not line:
                break
            text_message = line.rstrip("\n")
            if text_message.strip() == "":
                continue
            broadcast_message(f"{user_name}: {text_message}")
    finally:
        with connected_clients_lock:
            for c in list(connected_clients):
                if c["socket"] is client_socket:
                    connected_clients.remove(c)
                    break
        try:
            client_file.close()
        except Exception:
            pass
        try:
            client_socket.close()
        except Exception:
            pass
        broadcast_message(f"[СИСТЕМА] Пользователь {user_name} покинул чат.")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(10)
    print(f"Чат-сервер запущен на {SERVER_HOST}:{SERVER_PORT}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            t = threading.Thread(target=handle_client_connection, args=(client_socket, client_address), daemon=True)
            t.start()
    except KeyboardInterrupt:
        print("\nСервер остановлен пользователем.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
```

### Клиент 
```python
import socket
import threading

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9092

def receive_messages_loop(client_socket):
    client_file = client_socket.makefile("r", encoding="utf-8", newline="\n")
    try:
        for line in client_file:
            print(line.rstrip("\n"))
    finally:
        try:
            client_file.close()
        except Exception:
            pass

def main():
    print("Простой чат. Для выхода введите /quit")
    user_name = input("Введите имя: ").strip()
    if not user_name:
        print("Имя не может быть пустым.")
        return

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((SERVER_HOST, SERVER_PORT))
    except ConnectionRefusedError:
        print("Сервер недоступен.")
        return

    sock.sendall((user_name + "\n").encode("utf-8"))

    t = threading.Thread(target=receive_messages_loop, args=(sock,), daemon=True)
    t.start()

    try:
        while True:
            text = input()
            if text.strip().lower() == "/quit":
                break
            try:
                sock.sendall((text + "\n").encode("utf-8"))
            except Exception:
                print("Соединение потеряно.")
                break
    finally:
        try:
            sock.close()
        except Exception:
            pass
        print("Вы вышли из чата.")

if __name__ == "__main__":
    main()
```

---

## Подробное пояснение

### 1) Что делает сервер
- Создаёт TCP-сокет (`AF_INET` + `SOCK_STREAM`), вешается на адрес `127.0.0.1:9092`, начинает слушать (`listen(10)`).
- Для **каждого нового клиента** делает `accept()` и запускает **отдельный поток** `handle_client_connection`.
- Поток:
  1. Считывает **первую строку** — имя пользователя.
  2. Добавляет клиента в общий список `connected_clients` под защитой `Lock`.
  3. В бесконечном цикле читает **одну строку = одно сообщение** (`readline()`), и вызывает `broadcast_message`, чтобы разослать строку всем.
  4. При разрыве соединения удаляет клиента из списка и отправляет системное сообщение об уходе.

Почему так:
- **TCP** даёт нам надёжность и сохранение порядка сообщений, поэтому можно опираться на построчный обмен.
- **threading** позволяет обслуживать несколько клиентов одновременно: если один завис — другие не страдают.

### 2) Как устроен «протокол» чата
-  **каждое сообщение — отдельная строка**, заканчивается `\n`.
- В момент подключения клиент **первой строкой** отправляет имя пользователя.
- Все последующие строки считаются пользовательскими сообщениями.
- На сервере для чтения строк используем `makefile(...).readline()` — это удобно и просто.


### 3) Зачем нужен `Lock`
- Список клиентов — общий ресурс для всех потоков; его могут одновременно читать/менять разные потоки.
- Без блокировки возможны «гонки» и падения (например, один поток итерируется по списку, другой в этот момент удаляет элемент).
- Поэтому **любой доступ на изменение** выполняем внутри `with connected_clients_lock:`.

### 4) Клиент: почему два потока
- Основной поток **читает ввод** пользователя (`input()`) и отправляет строки на сервер.
- Отдельный фоновый поток **постоянно принимает** сообщения от сервера и печатает их.  
  Без него вы бы не видели входящие сообщения, пока ждёте `input()`.



