import socket
import threading
from dataclasses import dataclass
from datetime import datetime


class Config:
    HOST = "0.0.0.0"
    PORT = 8004
    BUFFER_SIZE = 1024


@dataclass
class ClientInfo:
    socket: socket.socket
    address: tuple
    nickname: str


clients: dict[socket.socket, ClientInfo] = {}


def broadcast_message(message: str, sender_socket: socket.socket | None = None) -> None:
    recipients = filter(lambda item: item[0] != sender_socket, clients.items())
    for client_socket, _ in recipients:
        try:
            client_socket.send(message.encode("utf-8"))
        except Exception:
            remove_client(client_socket)


def remove_client(client_socket: socket.socket) -> None:
    if client_socket not in clients:
        return

    nickname = clients[client_socket].nickname
    del clients[client_socket]

    leave_message = f"{nickname} покинул чат"
    broadcast_message(leave_message)
    print(leave_message)

    client_socket.close()


def handle_client(client_socket: socket.socket, client_address: tuple) -> None:
    nickname_data = client_socket.recv(Config.BUFFER_SIZE)
    nickname = nickname_data.decode("utf-8")

    clients[client_socket] = ClientInfo(client_socket, client_address, nickname)

    join_message = f"{nickname} присоединился к чату"
    print(f"{client_address[0]}:{client_address[1]} -> {join_message}")
    broadcast_message(join_message, client_socket)

    welcome_message = f"Добро пожаловать в чат, {nickname}!"
    client_socket.send(welcome_message.encode("utf-8"))

    while True:
        data = client_socket.recv(Config.BUFFER_SIZE)
        if not data:
            break

        message = data.decode("utf-8")
        if message.lower() == "exit":
            break

        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {nickname}: {message}"

        print(f"{client_address[0]}:{client_address[1]} -> {formatted_message}")
        broadcast_message(formatted_message, client_socket)


def client_to_thread(client_socket: socket.socket, client_address: tuple) -> None:
    def run() -> None:
        try:
            handle_client(client_socket, client_address)
        except Exception as e:
            print(f"Ошибка при обработке клиента {client_address}: {str(e)}")
        finally:
            remove_client(client_socket)

    client_thread = threading.Thread(target=run)
    client_thread.daemon = True
    client_thread.start()


def run_server() -> None:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((Config.HOST, Config.PORT))
    server_socket.listen(10)

    print(f"Сервер чата запущен на {Config.HOST}:{Config.PORT}")
    print("Ожидание подключений...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Подключение от {client_address[0]}:{client_address[1]}")

            client_to_thread(client_socket, client_address)

    except KeyboardInterrupt:
        print("\nЗавершение работы сервера...")
    finally:
        for client_socket in list(clients.keys()):
            client_socket.close()
        server_socket.close()
        print("Сервер остановлен")


if __name__ == "__main__":
    run_server()
