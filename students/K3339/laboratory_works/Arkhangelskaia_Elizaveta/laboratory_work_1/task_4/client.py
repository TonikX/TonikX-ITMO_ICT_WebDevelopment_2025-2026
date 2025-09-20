import socket
import threading
import sys

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8080

def listen_for_messages(sock):
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                print("[INFO] Соединение с сервером закрыто.")
                break
            sys.stdout.write(data.decode("utf-8"))
            sys.stdout.flush()
        except:
            break

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_HOST, SERVER_PORT))

    name = input("Enter your name: ")
    if not name:
        name = "Anonymous"
    sock.sendall((name + "\n").encode("utf-8"))

    threading.Thread(target=listen_for_messages, args=(sock,), daemon=True).start()

    try:
        while True:
            line = input()
            line = line.encode("utf-8", errors="replace").decode("utf-8")
            sock.sendall((line + "\n").encode("utf-8"))
    except (KeyboardInterrupt, EOFError):
        print("\n[INFO] Выход...")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
