import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 9997

def reader(sock, stop_event):
    """Поток чтения сообщений от сервера."""
    while not stop_event.is_set():
        try:
            data = sock.recv(4096)
            if not data:
                break
            print(data.decode("utf-8", errors="replace"), end="")
        except OSError:
            break

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        nickname = input("Введите ваш ник: ").strip()
        if not nickname:
            nickname = "anon"
        s.sendall(nickname.encode("utf-8"))

        stop_event = threading.Event()
        t = threading.Thread(target=reader, args=(s, stop_event))
        t.start()

        try:
            while True:
                line = sys.stdin.readline()
                if not line:
                    break
                s.sendall(line.encode("utf-8"))
                if line.strip().lower() == "/quit":
                    break
        except KeyboardInterrupt:
            pass

        stop_event.set()
        try:
            s.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass

        t.join()

if __name__ == "__main__":
    main()
