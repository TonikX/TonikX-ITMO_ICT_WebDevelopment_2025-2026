import socket
import threading

# Блокировка для безопасной работы с clients из разных потоков
clients = {}  # {socket: name}
clients_lock = threading.Lock()

def broadcast(message, sender_socket=None):
    with clients_lock:
        receivers = [c for c in clients.keys() if c != sender_socket]
        for client in receivers:
            try:
                client.sendall(message.encode("UTF-8"))
            except (ConnectionResetError, ConnectionAbortedError, OSError) as e:
                print(f"Ошибка соединения: {e}")
                client.close()
                with clients_lock:
                    clients.pop(client, None)

def handle_client(sock, address):
    try:
        sock.send("Введите имя: ".encode('UTF-8'))
        name = sock.recv(1024).decode('UTF-8').strip()
        # регистрируем клиента
        with clients_lock:
            clients[sock] = name
        sock.send("Вы подключились к чату. Наберите сообщение.".encode('UTF-8'))
        broadcast(f"Пользователь {name} присоединился к чату.", sender_socket=sock)

        while True:
            client_msg = sock.recv(1024)
            if not client_msg:
                break # Если пусто - клиент отключился
            broadcast(f"{name}: {client_msg.decode('UTF-8').strip()}", sender_socket=sock)
    finally:
        with clients_lock:
            username = clients.pop(sock, 'Неизвестный')  # Удаляем пользователя
        broadcast(f"Пользователь  {username} вышел из чата.")
        sock.close()



def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('127.0.0.1', 11111))
        server_socket.listen()
        print("Сервер запущен на 127.0.0.1:11111")

        while True:
            client_socket, client_address = server_socket.accept()
            # Для каждого клиента запускаем отдельный поток
            threading.Thread(
                target=handle_client,
                args=(client_socket, client_address),
                daemon=True
            ).start()

if __name__ == "__main__":
    run_server()