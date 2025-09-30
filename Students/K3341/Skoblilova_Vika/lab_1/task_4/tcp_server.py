import socket
import threading

HOST = "127.0.0.1"
PORT = 5007

clients = []
nicknames = []

def broadcast(message, sender_socket=None):
    for client in clients:
        if client != sender_socket:
            client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if not message:
                break

            index = clients.index(client)
            nickname = nicknames[index]
            full_message = f"[{nickname}]: {message}\n"
            print(full_message.strip())
            broadcast(full_message.encode("utf-8"), client)

        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames.pop(index)
                broadcast(f"{nickname} покинул чат.\n".encode("utf-8"))
            break

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Сервер запущен на {HOST}:{PORT}")

    while True:
        client, addr = server.accept()
        print(f"Подключение от {addr}")

        client.send("Введите ваш никнейм: ".encode("utf-8"))
        nickname = client.recv(1024).decode("utf-8")

        clients.append(client)
        nicknames.append(nickname)

        print(f"Пользователь {nickname} подключился.")
        broadcast(f"{nickname} присоединился к чату!\n".encode("utf-8"))
        client.send("Вы подключены к чату!\n".encode("utf-8"))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    start_server()
