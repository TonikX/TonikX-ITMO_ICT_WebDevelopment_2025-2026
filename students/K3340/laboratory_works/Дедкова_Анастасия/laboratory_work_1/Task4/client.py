import socket
import threading

HOST = "127.0.0.1"
PORT = 9094

print_lock = threading.Lock()


def receiver(sock: socket.socket) -> None:
    """Читает входящие сообщения и печатает их с новой строки."""
    try:
        while True:
            data = sock.recv(4096)
            if not data:
                with print_lock:
                    print("\n[Соединение закрыто сервером]")
                break
            text = data.decode("utf-8")
            with print_lock:
                # печатаем входящее и возвращаем
                print(f"\n{text}", end="")
                print("> ", end="", flush=True)
    except OSError:
        pass
    finally:
        try:
            sock.close()
        except OSError:
            pass


def main() -> None:
    nickname = input("Введите ник: ").strip() or "user"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    # отправляем ник первой строкой
    sock.sendall((nickname + "\n").encode("utf-8"))

    # запускаем поток-приёмник
    threading.Thread(target=receiver, args=(sock,), daemon=True).start()

    #Чтобы было можно печать во время отправки сообщений
    with print_lock:
        print("> ", end="", flush=True)

    try:
        while True:
            msg = input()
            if msg.strip().lower() == "/quit":
                sock.sendall(b"/quit\n")
                break
            sock.sendall((msg + "\n").encode("utf-8"))
            with print_lock:
                print("> ", end="", flush=True)
    except KeyboardInterrupt:
        pass
    finally:
        try:
            sock.close()
        except OSError:
            pass
        with print_lock:
            print("\nКлиент завершил работу")


if __name__ == "__main__":
    main()
