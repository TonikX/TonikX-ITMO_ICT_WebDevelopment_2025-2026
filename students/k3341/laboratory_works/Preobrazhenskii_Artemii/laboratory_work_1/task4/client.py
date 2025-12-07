import socket
import threading


def get_msg(client_socket):
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if msg:
                print(msg)
        except ConnectionResetError:
            print("\nНет соединения с сервером")


def run_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))

    name = input('Введите имя: ')
    client_socket.sendall(name.encode())

    threading.Thread(target=get_msg, args=(client_socket,), daemon=True).start()
    try:
        while True:
            msg = input()
            client_socket.sendall(msg.encode())
    except KeyboardInterrupt:
        print("\nВыход")
    finally:
        client_socket.close()

if __name__ == "__main__":
    run_client()