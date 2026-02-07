# chat_server.py
import socket
import threading

# Глобальный список подключённых клиентов: (client_socket, address)
clients = []
clients_lock = threading.Lock()  # Для безопасного доступа из нескольких потоков


def broadcast(message, sender_socket=None):
    """Рассылает сообщение всем клиентам, кроме отправителя (если указан)"""
    with clients_lock:
        for client_socket, _ in clients[:]:  # Копия списка на случай удаления
            if client_socket != sender_socket:
                try:
                    client_socket.send(message)
                except Exception:
                    # Если клиент отключился — удаляем его
                    client_socket.close()
                    clients[:] = [(sock, addr) for sock, addr in clients if sock != client_socket]


def handle_client(client_socket, address):
    """Обрабатывает одного клиента в отдельном потоке"""
    print(f"[+] Новое подключение: {address}")
    with clients_lock:
        clients.append((client_socket, address))

    try:
        while True:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"[{address}] {message.decode('utf-8', errors='replace')}")
            broadcast(message, sender_socket=client_socket)
    except ConnectionResetError:
        pass
    finally:
        with clients_lock:
            clients[:] = [(sock, addr) for sock, addr in clients if sock != client_socket]
        client_socket.close()
        print(f"[-] Клиент отключён: {address}")


def main():
    HOST = 'localhost'
    PORT = 12345

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[*] Сервер запущен на {HOST}:{PORT}")

    try:
        while True:
            client_socket, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            thread.daemon = True  # Поток завершится при выходе из main
            thread.start()
    except KeyboardInterrupt:
        print("\n[!] Сервер остановлен.")
    finally:
        server.close()


if __name__ == "__main__":
    main()