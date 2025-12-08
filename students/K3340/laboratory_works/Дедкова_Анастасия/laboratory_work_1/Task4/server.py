import socket
import threading

HOST = "127.0.0.1"
PORT = 9094

clients = []
nicknames = {}
lock = threading.Lock()


def broadcast(text, sender=None):
    """Отправка текстового сообщения всем клиентам."""
    dead = []
    with lock:
        for sock in clients:
            if sender is not None and sock is sender:
                continue
            try:
                sock.sendall((text + "\n").encode("utf-8"))
            except OSError:
                dead.append(sock)
        for s in dead:
            if s in clients:
                clients.remove(s)
            nicknames.pop(s, None)
            try:
                s.close()
            except OSError:
                pass


def handle_client(sock, addr):
    """Обработка одного клиента в отдельном потоке."""
    try:
        # первая полученная строка — ник
        raw = sock.recv(1024)
        nickname = raw.decode("utf-8").strip() if raw else ""
        if not nickname:
            nickname = f"user_{addr[1]}"

        with lock:
            clients.append(sock)
            nicknames[sock] = nickname

        broadcast(f"[+] {nickname} присоединился")
        print(f"{addr} -> {nickname}")

        while True:
            data = sock.recv(4096)
            if not data:
                break
            msg = data.decode("utf-8").rstrip("\r\n")
            if msg.lower() == "/quit":
                break
            broadcast(f"{nickname}: {msg}", sender=sock)
    except OSError:
        pass
    finally:
        with lock:
            if sock in clients:
                clients.remove(sock)
            name = nicknames.pop(sock, "unknown")
        broadcast(f"[-] {name} вышел")
        try:
            sock.close()
        except OSError:
            pass
        print(f"{addr} disconnected")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(10)
    print(f"Сервер: {HOST}:{PORT}")

    try:
        while True:
            client_sock, client_addr = server.accept()
            threading.Thread(
                target=handle_client, args=(client_sock, client_addr), daemon=True
            ).start()
    except KeyboardInterrupt:
        print("\nСтоп")
    finally:
        with lock:
            for s in clients:
                try:
                    s.close()
                except OSError:
                    pass
            clients.clear()
            nicknames.clear()
        server.close()


if __name__ == "__main__":
    main()
