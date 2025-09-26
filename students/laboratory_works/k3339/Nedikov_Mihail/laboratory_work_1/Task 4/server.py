import socket
import threading
from utils import send_json, recv_json

HOST, PORT = "127.0.0.1", 9090
clients = {}
lock = threading.Lock()


def broadcast(sender_conn, obj, include_sender=False):
    """Отправляет сообщение всем клиентам, кроме отправителя по умолчанию."""
    with lock:
        targets = [c for c in clients.keys() if include_sender or c is not sender_conn]

    dead = []
    for connection in targets:
        try:
            send_json(connection, obj)
        except Exception:
            dead.append(connection)

    if dead:
        with lock:
            for connection in dead:
                if connection in clients:
                    clients.pop(connection, None)
                try:
                    connection.close()
                except Exception:
                    pass


def handle_client(conn, addr):
    """Регистрирует клиента, читает его сообщения и отправляет их в чат."""
    print("Подключился:", addr)
    nick = None
    try:
        hello = recv_json(conn)
        if hello and hello.get("type") == "join":
            nick = hello.get("user", f"User{addr[1]}")
            with lock:
                clients[conn] = nick
            broadcast(
                conn,
                {"type": "system", "text": f"*** {nick} зашел в чат"},
                include_sender=True,
            )
        while True:
            msg = recv_json(conn)
            if msg is None:
                break
            if msg.get("type") == "leave":
                break
            print(f"{nick}: {msg}")
            broadcast(conn, {"type": "chat", "user": nick, "text": msg.get("text", "")})
    finally:
        left_nick = None
        with lock:
            if conn in clients:
                left_nick = clients.pop(conn)
        if left_nick:
            broadcast(conn, {"type": "system", "text": f"*** {left_nick} вышел из чата"})
        try:
            conn.close()
        except Exception:
            pass


def main():
    """Запускает TCP-сервер и создает поток на каждого подключившегося клиента."""
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
