import socket
import threading
from students.k3339.Shafikov_Maxim.Lr1.config import host, port

ENC = "utf-8"

# conn -> nickname
clients = {}
clients_lock = threading.Lock()


def send_line(conn, text: str):
    try:
        conn.sendall((text + "\n").encode(ENC))
    except OSError:
        pass


def broadcast(text: str, exclude=None):
    with clients_lock:
        dead = []
        for c in list(clients.keys()):
            if c is exclude:
                continue
            try:
                c.sendall((text + "\n").encode(ENC))
            except OSError:
                dead.append(c)
        for d in dead:
            name = clients.pop(d, None)
            try:
                d.close()
            except OSError:
                pass


def handle_client(conn: socket.socket, addr):
    name = None
    try:
        f = conn.makefile("r", encoding=ENC, newline="\n")

        # Выбор ника
        while True:
            send_line(conn, "Введите ник: ")
            name_line = f.readline()
            if not name_line:
                return
            candidate = name_line.strip()
            if not candidate:
                send_line(conn, "❌ Ник не может быть пустым.")
                continue
            with clients_lock:
                if candidate in clients.values():
                    send_line(conn, "❌ Ник уже занят. Попробуйте другой.")
                else:
                    name = candidate
                    clients[conn] = name
                    break

        send_line(conn, f"✅ Добро пожаловать, {name}! Напишите /quit для выхода.")
        broadcast(f"🟢 {name} присоединился к чату.", exclude=None)

        for line in f:
            msg = line.rstrip("\n")
            if not msg:
                continue
            if msg.strip().lower() == "/quit":
                send_line(conn, "Пока! Вы вышли из чата.")
                break
            broadcast(f"[{name}]: {msg}", exclude=conn)

    except Exception:
        pass
    finally:
        with clients_lock:
            if conn in clients:
                left_name = clients.pop(conn)
                broadcast(f"🔴 {left_name} покинул чат.", exclude=None)
        try:
            conn.close()
        except OSError:
            pass


def main():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_socket.bind((host, port))
    tcp_socket.listen()
    print(f"Сервер запущен на {host}:{port}")

    try:
        while True:
            conn, addr = tcp_socket.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\nОстановка сервера...")
    finally:
        tcp_socket.close()


if __name__ == "__main__":
    main()
