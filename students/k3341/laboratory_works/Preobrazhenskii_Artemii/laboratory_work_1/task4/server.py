import socket
import threading

clients = []

def connect_client(client_conn, client_addr):
    try:
        name = client_conn.recv(1024).decode('utf-8').strip()
        if not name:
            client_conn.close()
            return
        clients.append(client_conn)
        print(f'{name}{client_addr} подключился к чату')

        while True:
            msg = client_conn.recv(1024)
            if not msg:
                break
            text = msg.decode()
            broadcast(name, text, client_conn)
    finally:
        if client_conn in clients:
            clients.remove(client_conn)
        client_conn.close()
        print(f'{name} отключился')
    
def broadcast(name, text, client_conn):
    for client in clients:
        if client != client_conn:
             client.sendall(f'({name}): {text}'.encode())

def run_server():
    print('Сервер запущен')
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    server_socket.bind(('localhost', 8080))
    server_socket.listen()
    try:
        while True:
            client_conn, client_addr = server_socket.accept()
            threading.Thread(target=connect_client, args=(client_conn, client_addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\nСервер остановлен")
    finally:
        for client in clients:
            client.close()
        server_socket.close()

if __name__ == "__main__":
    run_server()



