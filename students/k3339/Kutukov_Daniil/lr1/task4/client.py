import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 50000

def receive_loop(sock):
    try:
        while True:
            data = sock.recv(4096)
            if not data:
                print("Соединение закрыто сервером.")
                break
            print(data.decode("utf-8"), end="")
    except Exception as e:
        print("Ошибка при получении:", e)
    finally:
        try:
            sock.close()
        except:
            pass
        sys.exit(0)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        t = threading.Thread(target=receive_loop, args=(sock,), daemon=True)
        t.start()

        try:
            while True:
                line = input()
                if line.strip() == "":
                    continue
                sock.sendall(line.encode("utf-8"))
                if line == "/quit":
                    break
        except (KeyboardInterrupt, EOFError):
            sock.sendall("/quit".encode("utf-8"))

if __name__ == "__main__":
    main()