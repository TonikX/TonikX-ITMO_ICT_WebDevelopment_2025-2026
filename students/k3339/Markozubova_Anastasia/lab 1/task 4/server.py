import socket
import threading

HOST = '0.0.0.0'
PORT = 9555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()
print(f'Server listening on {HOST}:{PORT}')

clients = []
nicknames = []
clients_lock = threading.Lock()

def broadcast(message: bytes):
    with clients_lock:
        for client in clients:
            try:
                client.sendall(message)
            except:
                   pass

def handle(client: socket.socket):
    while True:
        try:
            data = client.recv(1024)
            if not data:
                raise ConnectionResetError
            with clients_lock:
                idx = clients.index(client)
                nickname = nicknames[idx]
            message = f'{nickname}: {data.decode("utf-8")}\n'
            broadcast(message.encode('utf-8'))
        except:
            with clients_lock:
                if client in clients:
                    idx = clients.index(client)
                    clients.remove(client)
                    nickname = nicknames.pop(idx)
                else:
                    nickname = 'unknown'
            try:
                client.close()
            finally:
                broadcast(f'{nickname} left the chat.\n'.encode('utf-8'))
                print(f'{nickname} left the chat.')

            break
def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {address}')

        try:
            client.sendall(b'NICK')
            nickname = client.recv(1024).decode('utf-8').strip()
        except:
            client.close()
            continue

        with clients_lock:
            clients.append(client)
            nicknames.append(nickname)

        print(f'Nickname is {nickname}')
        broadcast(f'{nickname} joined the chat.\n'.encode('utf-8'))
        client.sendall(b'Connected to server!\n')

        threading.Thread(target=handle, args=(client,), daemon=True).start()

if __name__ == '__main__':
    try:
        receive()
    except KeyboardInterrupt:
        print('\nShutting down...')
    finally:
        with clients_lock:
            for c in clients:
                c.close()
        server.close()

