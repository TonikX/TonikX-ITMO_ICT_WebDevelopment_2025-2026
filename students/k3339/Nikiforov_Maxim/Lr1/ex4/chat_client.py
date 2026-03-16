import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 9090
ENC = "utf-8"
MAX_LINE = 800

def recv_loop(sock: socket.socket):
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                print("\n[disconnected]")
                break
            try:
                print(data.decode(ENC), end="")
            except UnicodeDecodeError:
                pass
    except OSError:
        pass
    finally:
        try:
            sock.close()
        except OSError:
            pass

def safe_line(s: str) -> str:
    s = s.replace("\r", " ").replace("\n", " ")
    return s[:MAX_LINE]

def main():
    name = input("Введите ваш ник: ").strip()
    if not name:
        print("Ник не может быть пустым.")
        sys.exit(1)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
    except OSError as e:
        print(f"Не удалось подключиться: {e}")
        sys.exit(1)

    # запускаем поток-приёмник
    t = threading.Thread(target=recv_loop, args=(sock,), daemon=True)
    t.start()

    try:
        # первая строка — ник
        sock.sendall((safe_line(name) + "\n").encode(ENC))
        # далее — сообщения пользователя
        while True:
            try:
                line = input()
            except (EOFError, KeyboardInterrupt):
                line = "/quit"
            line = line.strip()
            if not line:
                continue
            line = safe_line(line)
            sock.sendall((line + "\n").encode(ENC))
            if line == "/quit":
                break
    except OSError:
        pass
    finally:
        try:
            sock.close()
        except OSError:
            pass

if __name__ == "__main__":
    main()
