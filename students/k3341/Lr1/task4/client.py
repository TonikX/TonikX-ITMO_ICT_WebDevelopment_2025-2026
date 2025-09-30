import socket
import threading
import sys

SERVER_ADDRESS = "localhost"
SERVER_PORT = 8080
BUF_SIZE = 4096


def listen_for_messages(sock: socket.socket):
    while True:
        try:
            data = sock.recv(BUF_SIZE)
            if not data:
                print("[CLIENT] Server connection closed.")
                break
            sys.stdout.write(data.decode())
            sys.stdout.flush()
        except:
            break


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_ADDRESS, SERVER_PORT))

    name = input("Enter your name: ")
    if not name:
        name = "userAnon"
    sock.sendall((name + "\n").encode("utf-8"))

    threading.Thread(target=listen_for_messages, args=(sock,), daemon=True).start()

    try:
        while True:
            line = input()
            sock.sendall((line + "\n").encode())
    except (KeyboardInterrupt, EOFError):
        print("\n[CLIENT] Stopped.")
    finally:
        sock.close()


if __name__ == "__main__":
    main()
