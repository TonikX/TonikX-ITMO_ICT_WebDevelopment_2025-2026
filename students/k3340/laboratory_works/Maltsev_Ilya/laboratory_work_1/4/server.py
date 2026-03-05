import socket
import threading


class Connection:
    def __init__(self, sock: socket.socket, addr: tuple[str, int]):
        self.sock = sock
        self.addr = addr
        self.sock.settimeout(1)
        self.is_disconnected = False

    def close(self):
        self.is_disconnected = True
        self.sock.close()


class HandlerThread(threading.Thread):
    def __init__(self, connection: Connection, lock: threading.Lock, connections: list):
        super().__init__()
        self.connection = connection
        self.stop_event = threading.Event()
        self.lock = lock
        self.connections = connections

    def run(self) -> None:
        self.notify_all("Присоединился к чату")

        while not self.stop_event.is_set():
            try:
                msg = self.connection.sock.recv(1024).decode()
                if not msg:
                    break
                self.notify_all(msg)
            except socket.timeout:
                continue
            except (OSError, ConnectionResetError):
                break

        self.remove_connection()

    def remove_connection(self):
        self.connection.close()
        with self.lock:
            if self.connection in self.connections:
                self.connections.remove(self.connection)
        self.notify_all("Покинул чат")
        self.stop_event.set()

    def notify_all(self, msg: str) -> None:
        with self.lock:
            for conn in self.connections[:]:
                if conn != self.connection and not conn.is_disconnected:
                    try:
                        conn.sock.send(
                            f"{self.connection.addr[0]}:{self.connection.addr[1]} : {msg}".encode()
                        )
                    except (socket.timeout, OSError):
                        pass


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 8080))
server.listen(10)
server.settimeout(1)

active_connections = []
lock = threading.Lock()

try:
    while True:
        try:
            sock, addr = server.accept()
            conn = Connection(sock, addr)
            with lock:
                active_connections.append(conn)
            handler_thread = HandlerThread(conn, lock, active_connections)
            handler_thread.start()
        except socket.timeout:
            pass
except KeyboardInterrupt:
    print("\nВыключение сервера...")
    with lock:
        for conn in active_connections:
            conn.close()
    server.close()
