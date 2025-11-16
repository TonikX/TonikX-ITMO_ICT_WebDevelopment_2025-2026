# server.py
import socket
import threading

HOST = '0.0.0.0'   # слушать на всех интерфейсах (или '127.0.0.1' для локального теста)
PORT = 5001        # порт сервера

clients_lock = threading.Lock()
clients = {}  # socket -> username

def broadcast(message: str, exclude_sock=None):
    """Отправить message всем подключенным клиентам, кроме exclude_sock (если задан)"""
    with clients_lock:
        for sock in list(clients.keys()):
            if sock is exclude_sock:
                continue
            try:
                sock.sendall(message.encode('utf-8'))
            except Exception:
                # Если отправка упала — закрываем соединение
                remove_client(sock)

def remove_client(sock):
    """Удалить клиента (и оповестить остальных)"""
    with clients_lock:
        username = clients.pop(sock, None)
    try:
        sock.close()
    except Exception:
        pass
    if username:
        msg = f"*** Пользователь {username} покинул чат ***\n"
        print(msg.strip())
        broadcast(msg)

def handle_client(conn: socket.socket, addr):
    """Поток обработки одного клиента"""
    print(f"[+] Connected: {addr}")
    try:
        # Первое сообщение от клиента — его имя
        conn.sendall("Введите ваше имя: ".encode('utf-8'))
        name_data = conn.recv(1024)
        if not name_data:
            conn.close()
            return
        username = name_data.decode('utf-8').strip()
        if not username:
            username = f"User{addr[1]}"

        with clients_lock:
            clients[conn] = username

        welcome = f"*** Добро пожаловать, {username}! Сейчас в чате {len(clients)} пользователей. ***\n"
        conn.sendall(welcome.encode('utf-8'))

        join_msg = f"*** Пользователь {username} вошёл в чат ***\n"
        broadcast(join_msg, exclude_sock=conn)
        print(join_msg.strip())

        # Основной цикл получения сообщений от клиента
        while True:
            data = conn.recv(4096)
            if not data:
                break
            text = data.decode('utf-8').strip()
            if not text:
                continue

            # Простая команда выхода
            if text.lower() in ('/quit', '/exit'):
                break

            # Команды сервера (пример: /users) можно добавить
            if text.lower() == '/users':
                with clients_lock:
                    users_list = ", ".join(clients.values())
                conn.sendall(f"Список пользователей: {users_list}\n".encode('utf-8'))
                continue

            # Broadcast: имя: сообщение
            message = f"{username}: {text}\n"
            print(message.strip())
            broadcast(message, exclude_sock=None)

    except ConnectionResetError:
        # Клиент резко закрыл соединение
        pass
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        remove_client(conn)
        print(f"[-] Disconnected: {addr}")

def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen(10)
    print(f"Chat server listening on {HOST}:{PORT}")

    try:
        while True:
            conn, addr = server_sock.accept()
            # Для каждого клиента создаём поток
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()
    except KeyboardInterrupt:
        print("\nServer stopping by user...")
    finally:
        with clients_lock:
            for s in list(clients.keys()):
                try:
                    s.close()
                except:
                    pass
            clients.clear()
        server_sock.close()

if __name__ == "__main__":
    main()
