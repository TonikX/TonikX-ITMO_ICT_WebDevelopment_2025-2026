import socket
import threading
from students.k3339.Shafikov_Maxim.Lr1.config import host, port


def recv_loop(sock: socket.socket):
    """Фоновый поток для приёма сообщений после входа в чат."""
    try:
        f = sock.makefile("r", encoding="utf-8", newline="\n")
        for line in f:
            print(line.rstrip("\n"))
    except Exception:
        pass
    finally:
        try:
            sock.close()
        except OSError:
            pass


def main():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((host, port))
    f = tcp_socket.makefile("r", encoding="utf-8", newline="\n")

    # Выбор ника
    while True:
        prompt = f.readline()
        if not prompt:
            print("Сервер закрыл соединение.")
            return
        print(prompt.strip())
        name = input("> ")
        tcp_socket.sendall((name + "\n").encode("utf-8"))
        reply = f.readline()
        if not reply:
            print("Сервер закрыл соединение.")
            return
        print(reply.strip())
        if reply.startswith("✅"):
            break

    t = threading.Thread(target=recv_loop, args=(tcp_socket,), daemon=True)
    t.start()

    try:
        while True:
            line = input()
            if not line:
                continue
            tcp_socket.sendall((line + "\n").encode("utf-8"))
            if line.strip().lower() == "/quit":
                break
    except KeyboardInterrupt:
        tcp_socket.sendall(("/quit\n").encode("utf-8"))
    finally:
        try:
            tcp_socket.close()
        except OSError:
            pass


if __name__ == "__main__":
    main()
