import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 12345


def receive_loop(sock: socket.socket):
    try:
        while True:
            data = sock.recv(4096)
            if not data:
                print("Соединение с сервером разорвано.")
                break
            print(data.decode("utf-8"), end="")
    except Exception:
        pass
    finally:
        try:
            sock.close()
        except Exception:
            pass
        sys.exit(0)


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((HOST, PORT))
        except Exception as e:
            print("Не удалось подключиться:", e)
            sys.exit(1)

        initial = sock.recv(1024).decode("utf-8")
        print(initial, end="")
        nick = input().strip()
        sock.sendall((nick + "\n").encode("utf-8"))

        recv_thread = threading.Thread(target=receive_loop, args=(sock,), daemon=True)
        recv_thread.start()

        try:
            while True:
                msg = input()
                if msg.strip() == "/quit":
                    sock.sendall("/quit\n".encode("utf-8"))
                    break
                try:
                    sock.sendall((msg + "\n").encode("utf-8"))
                except Exception:
                    print("Ошибка отправки — соединение потеряно.")
                    break
        except KeyboardInterrupt:
            sock.sendall("/quit\n".encode("utf-8"))
        finally:
            try:
                sock.close()
            except Exception:
                pass
            print("Вы вышли из чата.")
            sys.exit(0)
