import os
import socket
import threading
import sys

HOST = "localhost"
PORT = 12000

def reader(sock):
    while True:
        data = sock.recv(4096)
        if not data:
            print("\n[CLIENT] Соединение закрыто")
            os._exit(0) 
        sys.stdout.write(data.decode("utf-8", errors="replace"))
        sys.stdout.flush()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        threading.Thread(target=reader, args=(s,), daemon=True).start()
        # имя
        name = input()
        s.sendall((name + "\n").encode("utf-8"))
        while True:
            line = input()
            if not line:
                continue
            s.sendall((line + "\n").encode("utf-8"))
            if line.strip().lower() == "/quit":
                break

if __name__ == "__main__":
    main()
