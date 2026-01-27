import socket
import threading
from cfg import SERVER_HOST, SERVER_PORT, BUFFER_SIZE

clients = {}
clients_lock = threading.Lock()

def broadcast(message, sender_socket=None):
    with clients_lock:
        for client_socket in clients:
            if client_socket != sender_socket:
                try:
                    client_socket.send(message.encode('utf-8'))
                except:
                    pass

def handle_client(client_socket, client_address):
    try:
        username = client_socket.recv(BUFFER_SIZE).decode('utf-8')
        with clients_lock:
            clients[client_socket] = username
        
        print(f"[+] {username} присоединился к чату ({client_address})")
        broadcast(f"[СЕРВЕР] {username} присоединился к чату!")
    
        while True:
            message = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            if not message:
                break
            print(f"[{username}]: {message}")
            broadcast(f"[{username}]: {message}", client_socket)
    except Exception as e:
        print(f"[!] Ошибка: {e}")
    finally:
        with clients_lock:
            if client_socket in clients:
                username = clients[client_socket]
                del clients[client_socket]
                print(f"[-] {username} покинул чат")
                broadcast(f"[СЕРВЕР] {username} покинул чат")
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(1)
    
    print(f"[*] Сервер чата запущен на {SERVER_HOST}:{SERVER_PORT}")
    print("[*] Ожидание подключений...")
    
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"[+] Новое подключение: {client_address}")
            
            thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address)
            )
            thread.daemon = True
            thread.start()
            
    except KeyboardInterrupt:
        print("\n[!] Сервер остановлен")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
