import socket
import threading

HOST = 'localhost'
PORT = 8080


def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            print(message)
        except:
            print("Вы отключены от сервера.")
            sock.close()
            break


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    print(sock.recv(1024).decode())
    nickname = input("Ваше имя: ")
    sock.send(nickname.encode())

    thread = threading.Thread(target=receive_messages, args=(sock,))
    thread.start()

    while True:
        message = input()
        if message.lower() == '!q':
            sock.close()
            break
        sock.send(f"{nickname}: {message}".encode())


if __name__ == "__main__":
    main()
