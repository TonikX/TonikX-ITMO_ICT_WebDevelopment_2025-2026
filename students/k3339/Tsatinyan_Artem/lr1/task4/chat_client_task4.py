import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 7070
ENC = "utf-8"
BUF = 4096

def reader(sock: socket.socket):
    """
    Поток для чтения сообщений от сервера.
    Работает в фоне и сразу печатает все входящие данные.
    """
    try:
        while True:
            data = sock.recv(BUF)
            if not data:
                print("** Соединение закрыто сервером")
                break
            print(data.decode(ENC, errors="replace"), end="")
    except OSError:
        pass

def main():
    nickname = input("Введите ник: ").strip() or "anon"

    # Создаём TCP-сокет
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cli:
        cli.connect((HOST, PORT))
        # Отправляем свой ник
        cli.sendall(f"NICK:{nickname}\n".encode(ENC))

        # Запускаем поток для приёма сообщений
        t = threading.Thread(target=reader, args=(cli,), daemon=True)
        t.start()

        try:
            # Читаем ввод из stdin и отправляем серверу
            while True:
                line = sys.stdin.readline()
                if not line:
                    break
                cli.sendall(line.encode(ENC))
                if line.strip() == "/quit":
                    break
        except KeyboardInterrupt:
            try:
                cli.sendall(b"/quit\n")
            except OSError:
                pass

if __name__ == "__main__":
    main()
