import socket
import threading

clients = []
clients_lock = threading.Lock()


def handle_client(client_socket, address):
    
    print(f"[+] Подключился новый клиент: {address}")

    try:
        while True:
    
            message = client_socket.recv(1024).decode('utf-8')

            if not message:
                break

            print(f"Сообщение от {address}: {message}")

            message_to_send = f"[{address}] {message}"

            with clients_lock:
                for client in clients[:]:
                    if client != client_socket:
                        try:
                            client.send(message_to_send.encode('utf-8'))
                        except:
                            clients.remove(client)
    except (ConnectionResetError, BrokenPipeError):
        print(f"[-] Соединение с клиентом {address} было разорвано.")
    finally:
        with clients_lock:
            if client_socket in clients:
                clients.remove(client_socket)
                print(f"[-] Клиент {address} отключен. Активных клиентов: {len(clients)}")
        client_socket.close()


def start_server(host='localhost', port=12345):
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((host, port))

    server_socket.listen(5)
    print(f"[*] Сервер запущен на {host}:{port}. Ожидание подключений...")

    try:
        while True:
            client_socket, address = server_socket.accept()

            with clients_lock:
                clients.append(client_socket)
                print(f"[*] Активных клиентов: {len(clients)}")

            client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
            client_thread.daemon = True
            client_thread.start()

    except KeyboardInterrupt:
        print("\n[*] Остановка сервера...")
    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()