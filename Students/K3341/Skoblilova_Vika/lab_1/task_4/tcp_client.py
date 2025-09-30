import socket
import threading
import sys

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode("utf-8")
            if not msg:
                break
            print(msg)
        except:
            print("Соединение с сервером потеряно.")
            break

def main():
    host = "127.0.0.1"   
    port = 5007        

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((host, port))
    except ConnectionRefusedError:
        print(f"Не удалось подключиться к серверу {host}:{port}. "
            "Проверь, что сервер запущен.")
        sys.exit(1)
    except socket.error as e:
        print(f"Ошибка подключения: {e}")
        sys.exit(1)

    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

    print("Подключено к чату. Напишите сообщение (или 'exit' для выхода).")

    while True:
        msg = input()
        if msg.lower() == "exit":
            sock.close()
            break
        try:
            sock.send(msg.encode("utf-8"))
        except:
            print("Не удалось отправить сообщение. Соединение закрыто.")
            break

if __name__ == "__main__":
    main()
