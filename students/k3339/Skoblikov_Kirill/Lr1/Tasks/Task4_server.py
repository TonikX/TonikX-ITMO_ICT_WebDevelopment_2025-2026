import socket
import threading


class ChatServer:
    def __init__(self, host='localhost', port=8911):
        self.host = host
        self.port = port
        self.socket = None
        self.clients = {}
        self.lock = threading.Lock()
        self.guest_counter = 0
        self.is_running = False
        self.admin_thread = None

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        self.is_running = True

        self.admin_thread = threading.Thread(target=self.admin_loop, daemon=True)
        self.admin_thread.start()

        print(f"Сервер запущен на {self.host}:{self.port}")
        print("Административные команды:")
        print("  /server_off - остановить сервер")

        try:
            while self.is_running:
                try:
                    self.socket.settimeout(1.0)
                    client_socket, addr = self.socket.accept()

                    if not self.is_running:
                        client_socket.close()
                        break

                    print(f"Новое подключение: {addr}")
                    guest_name = f"Гость {self.guest_counter}"
                    self.guest_counter += 1

                    with self.lock:
                        self.clients[client_socket] = guest_name

                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, guest_name)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                except socket.timeout:
                    continue
                except OSError as e:
                    if self.is_running:
                        print(f"Ошибка сокета: {e}")
                    break
        except KeyboardInterrupt:
            print("Получен сигнал прерывания")
            self.stop()
        finally:
            if self.is_running:  # Если еще не остановлен
                self.stop()

    def handle_client(self, client_socket, username):
        self.broadcast(f"{username} присоединился к чату!", exclude=client_socket)
        client_socket.send(f"Добро пожаловать, {username}!".encode())

        while self.is_running:
            try:
                client_socket.settimeout(1.0)
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                if self.is_running:
                    self.broadcast(f"{username}: {message}", exclude=client_socket)
            except socket.timeout:
                continue
            except:
                break

        self.remove_client(client_socket, username)

    def broadcast(self, message, exclude=None):
        with self.lock:
            disconnected = []
            for client, username in self.clients.items():
                if client != exclude:
                    try:
                        client.send(message.encode())
                    except:
                        disconnected.append(client)

            for client in disconnected:
                if client in self.clients:
                    del self.clients[client]

    def remove_client(self, client_socket, username):
        with self.lock:
            if client_socket in self.clients:
                del self.clients[client_socket]
        if self.is_running:
            self.broadcast(f"{username} покинул чат!")

        client_socket.close()
        print(f"Клиент {username} отключен")

    def admin_loop(self):
        while self.is_running:
            command = input()
            if command == '/server_off':
                print("Остановка сервера...")
                self.stop()
                break

    def stop(self):
        self.is_running = False
        with self.lock:
            for client in list(self.clients.keys()):
                client.close()

            self.clients.clear()

        if self.socket:
            self.socket.close()
            self.socket = None

        print("Сервер остановлен")


if __name__ == "__main__":
    server = ChatServer()
    server.start()