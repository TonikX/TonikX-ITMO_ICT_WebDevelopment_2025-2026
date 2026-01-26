import socket
import threading

HOST = '127.0.0.1'
PORT = 9090

clients = {}  # {client_socket: client_address}


# отправка сообщений всем клиентам кроме отправителя
def broadcast(message, sender_socket):
    for client in list(clients.keys()):
        if client != sender_socket:
            try:
                client.send(message)
            except:
                del clients[client]


# обработка сообщений от конкертного клиента
def handle_client(client_socket):
    print(f"+ Подключен {clients[client_socket]}")
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"({clients[client_socket][0]}:{clients[client_socket][1]}) {message}")
            broadcast(f"({clients[client_socket][0]}:{clients[client_socket][1]}): {message}".encode('utf-8'), client_socket)
        except:
            break
    print(f"- Отключен {clients[client_socket]}")
    del clients[client_socket]
    client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"HTTP сервер запущен на http://{HOST}:{PORT}")

    while True:
        client_socket, client_address = server.accept()
        clients[client_socket] = client_address
        thread = threading.Thread(target=handle_client, args=(client_socket, ))
        thread.start()


if __name__ == "__main__":
    start_server()