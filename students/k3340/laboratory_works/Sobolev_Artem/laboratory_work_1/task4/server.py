import socket
import threading

SERVER_ADDRESS = ("127.0.0.1", 10000)

# Множество всех подключенных клиентов. Lock защищает его от одновременной записи из разных потоков
clients = set()
clients_lock = threading.Lock()

def add_client(sock):
    # Добавление клиента под Lock, чтобы защитить от гонки
    with clients_lock:
        clients.add(sock)

def remove_client(sock):
    with clients_lock:
        clients.discard(sock)

def broadcast(data, sender):
    # Копирование списка клиентов
    with clients_lock:
        targets = tuple(clients)

    # Рассылка сообщения всем клиента, кроме отправителя
    dead = []
    for client in targets:
        if client is sender:
            continue
        try:
            client.sendall(data)
        except (ConnectionResetError, ConnectionAbortedError, OSError):
            dead.append(client)
    # Если при отправке клиенту произошла ошибка, то соединение с ним закрываетсяя, он удаляется из клиента
    for client in dead:
        remove_client(client)
        try:
            client.close()
        except OSError:
            pass

# Каждый клиент работает в отдельном потоке
def handle_client(sock):
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                break
            broadcast(data, sock)
    finally:
        remove_client(sock)
        sock.close()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(SERVER_ADDRESS)
        server_socket.listen()

        while True:
            sock, addr = server_socket.accept()
            add_client(sock)
            # Клиент добавляет в отдельный поток
            threading.Thread(target=handle_client, args=(sock,), daemon=True).start()

if __name__ == "__main__":
    main()
