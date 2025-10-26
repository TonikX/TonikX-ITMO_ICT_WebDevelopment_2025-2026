import socket
import threading

users = []
k = 0

users_lock = threading.Lock()


def process_user(client_connection, client_address):
    global users
    while True:
        message = client_connection.recv(1024)

        with users_lock:
            for user in users:
                if user != client_connection:
                    try:
                        user.sendall(message)
                    except:
                        users.remove(user)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 8080))

server_socket.listen(5)
print("Чат запущен на порту 8080...")


while True:
    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    with users_lock:
        users.append(client_connection)
    k += 1

    name = client_connection.recv(1024).decode()
    with users_lock:
        for user in users:
            user.sendall(f"новый участник чата - {name}".encode())

    t = threading.Thread(target=process_user, args=(client_connection, client_address))
    t.start()

    print(f"новый поток для клиента {k - 1} запущен")