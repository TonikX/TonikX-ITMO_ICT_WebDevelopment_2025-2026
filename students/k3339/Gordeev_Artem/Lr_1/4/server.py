import socket
import threading


def broadcast(message: bytes, sender: socket.socket = None):
    for client in clients:
        if client == sender:
            continue
        try:
            client.sendall(message)
        except:
            remove_client(client)


def remove_client(client: socket.socket):
    if client in clients:
        index = clients.index(client)
        clients.remove(client)
        nickname = nicknames.pop(index)
        broadcast(f'{nickname} покинул(а) чат!'.encode('utf-8'))
        print(f'{nickname} отключился.')


# функция для работы с клиентом в отдельном потоке
def process_client(client: socket.socket):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                remove_client(client)
                break
            broadcast(message, client)
        except:
            remove_client(client)
            break


# AF_INET - IPv4, SOCK_STREAM - TCP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Решение проблемы Address already in use. Игнорирование состояния сокета TIME_WAIT
tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

tcp_socket.bind(('localhost', 9999))
tcp_socket.listen(5)

clients = []
nicknames = []

while True:
    client_socket, addr = tcp_socket.accept()
    print(f"Новое подключение от {str(addr)}")

    client_socket.sendall('NICK'.encode('utf-8'))
    nickname = client_socket.recv(1024).decode('utf-8')

    nicknames.append(nickname)
    clients.append(client_socket)

    print(f"Никнейм клиента: {nickname}")
    broadcast(f"{nickname} присоединился к чату!".encode('utf-8'))
    client_socket.sendall("Вы подключены к серверу!".encode('utf-8'))

    thread = threading.Thread(target=process_client, args=[client_socket])
    thread.start()
