import socket
import threading

HOST = '0.0.0.0'
PORT = 8080

clients_lock = threading.Lock()
clients = {}

def broadcast(message: bytes):
    with clients_lock:
        for sock in list(clients.keys()):
            try:
                sock.sendall(message)
            except:
                remove_client(sock)

def remove_client(sock):
    with clients_lock:
        name = clients.pop(sock, None)
    try:
        sock.close()
    except:
        pass
    if name:
        print(f'[DISCONNECT] {name}')
        broadcast(f'[SERVER] {name} покинул(а) чат.\n'.encode('utf-8'))

def handle_client(client_sock, addr):
    try:
        client_sock.sendall(b'Enter your name: ')
        name_bytes = recv_until_newline(client_sock)
        if not name_bytes:
            remove_client(client_sock)
            return
        username = name_bytes.decode('utf-8').strip()
        if not username:
            username = f'{addr[0]}:{addr[1]}'

        with clients_lock:
            clients[client_sock] = username

        print(f'[CONNECT] {username} подключен(а) с {addr}')
        broadcast(f'[SERVER] {username} присоединился(ась) к чату.\r\n'.encode('utf-8'))
        while True:
            data = recv_until_newline(client_sock)
            if not data:
                break
            text = data.decode('utf-8', errors='replace').rstrip('\n')
            message = f'{username}: {text}\n'
            print(f'[MSG] {message.strip()}')
            broadcast(message.encode('utf-8'))

    except Exception as e:
        print(f'[ERROR] Ошибка с клиентом {addr}: {e}')
    finally:
        remove_client(client_sock)

def recv_until_newline(sock):
    buffer = bytearray()
    try:
        while True:
            chunk = sock.recv(1024)
            if not chunk:
                return b''
            buffer.extend(chunk)
            if b'\n' in chunk:
                break
    except:
        return b''
    idx = buffer.find(b'\n') + 1
    return bytes(buffer[:idx])

def main():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(10)
    print(f'Сервер запущен на {HOST}:{PORT}. Ожидание подключений...')

    try:
        while True:
            client_sock, addr = srv.accept()
            thread = threading.Thread(target=handle_client, args=(client_sock, addr), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        print('\n[SHUTDOWN] Сервер завершает работу...')
    finally:
        with clients_lock:
            for s in list(clients.keys()):
                try:
                    s.shutdown(socket.SHUT_RDWR)
                    s.close()
                except:
                    pass
            clients.clear()
        srv.close()
        print('[SHUTDOWN]')

if __name__ == '__main__':
    main()
