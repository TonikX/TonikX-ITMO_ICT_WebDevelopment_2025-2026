import socket
import json
import threading

user_id = input()


def get_data(s):
    while True:
        data = s.recv(1024).decode()
        msg = json.loads(data)
        if msg['id'] != user_id:
            print(data)


def send_data(s):
    while True:
        msg = input()
        if msg:
            s.sendall(msg.encode())


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 8082))
    s.sendall(user_id.encode())
    threading.Thread(target=get_data, args=[s]).start()
    threading.Thread(target=send_data, args=[s]).start()


if __name__ == '__main__':
    main()
