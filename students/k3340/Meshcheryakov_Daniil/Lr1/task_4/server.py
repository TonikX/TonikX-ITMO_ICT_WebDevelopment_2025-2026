import socket, threading

HOST = "127.0.0.1"
PORT = 9997
clients = {}  # {conn: nickname}

def broadcast(msg, exclude=None):
    """Рассылает сообщение всем клиентам, кроме exclude."""
    for c in list(clients):
        if c is exclude:
            continue
        try:
            c.sendall(msg.encode("utf-8"))
        except:
            c.close()
            clients.pop(c, None)

def handle(conn):
    with conn:
        conn.sendall("Ник: ".encode("utf-8"))
        nick = conn.recv(1024).decode().strip() or "anon"
        clients[conn] = nick
        broadcast(f"* {nick} вошёл в чат *\n")

        while True:
            data = conn.recv(1024)
            if not data:
                break
            msg = data.decode().strip()

            if msg == "/quit":
                break

            if msg.startswith("/nickname "):
                new_nick = msg.partition(" ")[2].strip()
                if new_nick:
                    old_nick = clients[conn]
                    clients[conn] = new_nick
                    broadcast(f"* {old_nick} сменил ник на {new_nick} *\n")
                else:
                    conn.sendall("❌ Использование: /nickname новый_ник\n".encode("utf-8"))
                continue

            broadcast(f"[{clients[conn]}] {msg}\n")

        broadcast(f"* {clients[conn]} вышел из чата *\n")
        clients.pop(conn, None)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[CHAT SERVER] {HOST}:{PORT}")
        while True:
            conn, _ = s.accept()
            threading.Thread(target=handle, args=(conn,), daemon=True).start()

if __name__ == "__main__":
    main()
