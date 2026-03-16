import socket
import threading

HOST = "0.0.0.0"
PORT = 9090
BACKLOG = 20
ENC = "utf-8"
MAX_LINE = 800     # ограничение на длину одного сообщения (в символах)

clients = {}           # socket -> name
clients_lock = threading.Lock()

def broadcast(message: str, exclude_sock=None):
    """Отправить сообщение всем клиентам, кроме exclude_sock (если задан)."""
    data = message.encode(ENC, errors="ignore")
    dead = []
    with clients_lock:
        for sock in list(clients.keys()):
            if sock is exclude_sock:
                continue
            try:
                sock.sendall(data)
            except OSError:
                dead.append(sock)
        # подчистим умершие соединения
        for sock in dead:
            try:
                name = clients.pop(sock)
            except KeyError:
                name = None
            try:
                sock.close()
            except OSError:
                pass
            if name:
                # уведомим остальных, что клиент отвалился
                msg = f"* {name} left the chat\n"
                for s in list(clients.keys()):
                    try:
                        s.sendall(msg.encode(ENC))
                    except OSError:
                        pass

def safe_line(s: str) -> str:
    """Обрезаем переносы строк и длину."""
    s = s.replace("\r", "").replace("\n", "")
    if len(s) > MAX_LINE:
        s = s[:MAX_LINE]
    return s

def handle_client(conn: socket.socket, addr):
    conn.settimeout(300)
    buf = ""
    name = None
    try:
        # читаем имя
        while "\n" not in buf:
            chunk = conn.recv(1024)
            if not chunk:
                raise ConnectionError("client disconnected before sending name")
            buf += chunk.decode(ENC, errors="ignore")
        name, buf = buf.split("\n", 1)
        name = safe_line(name).strip() or f"user@{addr[0]}:{addr[1]}"

        # регистрируем юзера
        with clients_lock:
            clients[conn] = name
        conn.sendall(f"* Welcome, {name}! Type /quit to exit\n".encode(ENC))
        broadcast(f"* {name} joined the chat\n", exclude_sock=conn)

        # -основной цикл чтения строк
        while True:
            # если в буфере уже есть полная строка — обработаем
            if "\n" in buf:
                line, buf = buf.split("\n", 1)
            else:
                data = conn.recv(1024)
                if not data:
                    break
                buf += data.decode(ENC, errors="ignore")
                if "\n" not in buf:
                    continue
                line, buf = buf.split("\n", 1)

            text = safe_line(line)
            if not text:
                continue
            if text == "/quit":
                break

            broadcast(f"[{name}] {text}\n", exclude_sock=conn)

    except (ConnectionError, OSError, socket.timeout):
        # игнорируем детали — просто считаем, что клиент отвалился
        pass
    finally:
        # снятие регистрации, закрытие и уведомление остальных
        with clients_lock:
            user = clients.pop(conn, None)
        try:
            conn.close()
        except OSError:
            pass
        if user:
            broadcast(f"* {user} left the chat\n")

def main():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(BACKLOG)
    print(f"Chat server listening on {HOST}:{PORT} ...")

    try:
        while True:
            conn, addr = srv.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()
    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        # GS
        with clients_lock:
            for s in list(clients.keys()):
                try:
                    s.close()
                except OSError:
                    pass
            clients.clear()
        try:
            srv.close()
        except OSError:
            pass

if __name__ == "__main__":
    main()
