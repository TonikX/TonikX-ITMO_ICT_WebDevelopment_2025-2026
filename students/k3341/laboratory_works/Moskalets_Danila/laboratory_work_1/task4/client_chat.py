import socket
import threading

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9090


# получение сообщения от сервера
def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if message:
                print("\n" + message)
        except:
            print("Отключено от сервера.")
            break


def client_main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_HOST, SERVER_PORT))
    print("Подключено к серверу. Можете писать сообщения:")

    # запускаем поток для получения сообщений
    thread = threading.Thread(target=receive_messages, args=(sock,))
    thread.start()

    # отправка сообщений
    while True:
        msg = input()
        if msg.lower() == 'exit':
            break
        sock.send(msg.encode('utf-8'))

    sock.close()


if __name__ == "__main__":
    client_main()