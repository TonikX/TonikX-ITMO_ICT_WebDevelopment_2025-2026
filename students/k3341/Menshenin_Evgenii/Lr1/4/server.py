import socket
import threading
from chat.message_entity import Message

clients = {}


def new_client(conn):
    client_id = get_client_id(conn)
    print("New client id:", client_id)

    clients[client_id] = conn
    while True:
        message = conn.recv(1024).decode()
        if message:
            print("message received:", message)
            send_to_all(Message(client_id, message))


def get_client_id(conn) -> str:
    while True:
        client_id = conn.recv(1024).decode()
        print("Client id:", client_id)
        if client_id not in clients:
            clients[client_id] = conn
            break
        elif client_id in clients:
            print("wrong id", client_id)
            conn.send(b"id used")
    print("correct id", client_id)
    return client_id


def send_to_all(message: Message):
    msg = '{' + f'"id": "{message.id}", "msg": "{message.msg}"' + '}'
    for i in clients.keys():
        conn = clients[i]
        print(f"sending message to {i}:", msg)
        conn.sendall(msg.encode())


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 8082))
        s.listen()
        while True:
            conn, addr = s.accept()
            threading.Thread(target=new_client, args=[conn]).start()


if __name__ == '__main__':
    main()
