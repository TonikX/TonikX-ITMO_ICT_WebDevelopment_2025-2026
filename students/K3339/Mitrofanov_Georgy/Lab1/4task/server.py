import socket
import threading

clients = []
nicknames = []


def start_server(host="localhost", port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Сервер запущен на {host}:{port}")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Подключение от {address}")

        client_socket.send("NICK".encode("utf-8"))
        nickname = client_socket.recv(1024).decode("utf-8")

        nicknames.append(nickname)
        clients.append(client_socket)

        print(f"Никнейм клиента: {nickname}")
        broadcast(
            f"{nickname} присоединился к чату!".encode("utf-8"),
            client_socket,
            is_notif=True,
        )

        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()


def broadcast(message, client_socket, is_notif=False):
    response = ""
    for client in clients:
        if client != client_socket:
            if is_notif:
                response = message
            else:
                index = clients.index(client_socket)
                nickname = nicknames[index]
                response = f"\r{nickname} : ".encode("utf-8") + message
            try:
                client.send(response)
            except:
                remove_client(client)


def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                broadcast(message, client_socket)
            else:
                remove_client(client_socket)
                break
        except:
            remove_client(client_socket)
            break


def remove_client(client_socket):
    if client_socket in clients:
        index = clients.index(client_socket)
        nickname = nicknames[index]

        clients.remove(client_socket)
        nicknames.remove(nickname)

        broadcast(
            f"{nickname} покинул чат".encode("utf-8"), client_socket, is_notif=True
        )
        client_socket.close()


if __name__ == "__main__":
    start_server()
