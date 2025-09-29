import socket
import threading
import sys

HOST = "localhost"
PORT = 9091

def reader(sock: socket.socket):
    # Читает всё, что приходит с сервера, и печатает в консоль
    try:
        f = sock.makefile("r", encoding="utf-8", newline="\n")
        for line in f:
            print(line.rstrip("\n"))
    except Exception:
        pass
    finally:
        try:
            sock.close()
        except Exception:
            pass

def writer(sock: socket.socket):
    try:
        # Отправляем ник — первая строка, которую просит сервер
        nickname = input().strip()
        sock.sendall((nickname + "\n").encode("utf-8"))

        # Дальше читаем строки из stdin и отправляем
        for line in sys.stdin:
            line = line.rstrip("\n")
            sock.sendall((line + "\n").encode("utf-8"))
            if line == "/quit":
                break
    except (BrokenPipeError, OSError):
        pass
    finally:
        try:
            sock.close()
        except Exception:
            pass

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    # Приветственное приглашение сервера («Введите никнейм: »)
    greeting = sock.recv(1024).decode("utf-8")
    print(greeting, end="")

    t_r = threading.Thread(target=reader, args=(sock,), daemon=True)
    t_w = threading.Thread(target=writer, args=(sock,), daemon=False)

    t_r.start()
    t_w.start()
    t_w.join()   # Ждём завершения ввода пользователя

if __name__ == "__main__":
    main()
