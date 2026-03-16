import socket
import threading

HOST = "0.0.0.0"
PORT = 12345

clients = {}
clients_lock = threading.Lock()


def broadcast(message: str, exclude_sock=None):
    """Отправить message всем клиентам (кроме exclude_sock)."""
    with clients_lock:
        for sock in list(clients.keys()):
            if sock is exclude_sock:
                continue
            try:
                sock.sendall(message.encode("utf-8"))
            except Exception:
                remove_client(sock)


def remove_client(sock):
    with clients_lock:
        nick = clients.pop(sock, None)
    try:
        sock.close()
    except Exception:
        pass
    if nick:
        broadcast(f"[Сервер] Пользователь '{nick}' покинул чат.\n")


def handle_client(conn: socket.socket, addr):
    try:
        conn.sendall("Введите ваш ник: ".encode("utf-8"))
        nick = conn.recv(1024).decode("utf-8").strip()
        if not nick:
            conn.sendall("Неправильный ник, соединение закрывается.\n".encode("utf-8"))
            conn.close()
            return

        with clients_lock:
            clients[conn] = nick

        print(f"[+] {addr} -> {nick} присоединился")
        broadcast(
            f"[Сервер] Пользователь '{nick}' присоединился к чату.\n", exclude_sock=conn
        )
        conn.sendall(
            "[Сервер] Добро пожаловать! Введите сообщения. Для выхода введите /quit\n".encode(
                "utf-8"
            )
        )

        while True:
            data = conn.recv(4096)
            if not data:
                break
            text = data.decode("utf-8").rstrip("\n")
            if text == "/quit":
                break
            message = f"{nick}: {text}\n"
            print(message.strip())
            broadcast(message, exclude_sock=conn)

    except ConnectionResetError:
        pass
    except Exception as e:
        print("Ошибка в обработчике клиента:", e)
    finally:
        remove_client(conn)
        print(f"[-] {addr} отключился")


def accept_loop(server_sock: socket.socket):
    while True:
        conn, addr = server_sock.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((HOST, PORT))
        server_sock.listen()
        print(f"Сервер чата запущен на {HOST}:{PORT}")
        try:
            accept_loop(server_sock)
        except KeyboardInterrupt:
            print("\nСервер остановлен вручную.")
