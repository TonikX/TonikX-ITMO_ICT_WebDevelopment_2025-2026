import socket
import threading
import sys

SERVER_ADDRESS = ("127.0.0.1", 10000)

# Приём сообщений сообщений от сервера
def recv_loop(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("Соединение закрыто сервером")
                break
            print(data.decode("utf-8").strip())
        except (ConnectionResetError, ConnectionAbortedError, OSError):
            break

def start_process():
    if len(sys.argv) < 2:
        print("Использование: python client.py <имя>")
        return

    username = sys.argv[1]
    main(username)

def main(username: str):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(SERVER_ADDRESS)
        # Отдельный поток для постоянного приёма данных, чтобы клиент мог одновременно печатать сообщения и получать новые из чата
        threading.Thread(target=recv_loop, args=(client_socket,), daemon=True).start()
        while True:
            msg = input()
            if msg == "\\quit":
                break
            msg = f"{username}:" + msg
            client_socket.sendall((msg + "\n").encode("utf-8"))


if __name__ == "__main__":
    start_process()