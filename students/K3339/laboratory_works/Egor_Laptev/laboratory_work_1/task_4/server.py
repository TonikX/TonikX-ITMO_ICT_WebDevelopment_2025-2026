import socket
import threading

HOST = 'localhost'
PORT = 8080

clients = []
nicknames = []


def broadcast(message, _client=None):
    for client in clients:
        if client != _client:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)


def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                break
            broadcast(message, client)
        except:
            clients.remove(client)
            client.close()
            break


def receive_connections():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen()
    print(f"Сервер запущен на {HOST}:{PORT}")

    while True:
        client, addr = sock.accept()
        print(f"Подключился {addr}")
        client.send("Введите ваше имя: ".encode())
        nickname = client.recv(1024).decode()
        nicknames.append(nickname)
        clients.append(client)
        print(f"Пользователь {nickname} присоединился.")
        broadcast(f"{nickname} присоединился в чат.".encode(), client)

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    receive_connections()
