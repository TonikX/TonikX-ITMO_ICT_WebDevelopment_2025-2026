import socket
import threading
from utils import send_json, recv_json

HOST, PORT = "127.0.0.1", 9090

running = True  # Флаг, который завершает поток чтения при выходе.


def listen(sock):
    """Получает сообщения от сервера и выводит их пользователю."""
    global running
    while running:
        msg = recv_json(sock)
        if msg is None:
            break
        if msg["type"] == "system":
            print(msg["text"])
        elif msg["type"] == "chat":
            print(f"{msg['user']}: {msg['text']}")


def main():
    global running
    nick = input("Введите ваш ник: ")

    cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cli.connect((HOST, PORT))

    # Сообщаем серверу, что мы присоединились к чату.
    send_json(cli, {"type": "join", "user": nick})

    # Запускаем поток, который слушает сообщения от сервера.
    listener = threading.Thread(target=listen, args=(cli,))
    listener.start()

    while True:
        text = input()
        if text.strip().lower() == "/quit":
            # Предупреждаем сервер о выходе, если есть возможность.
            try:
                send_json(cli, {"type": "leave"})
            except Exception:
                pass
            running = False
            break
        send_json(cli, {"type": "chat", "text": text})

    cli.close()
    listener.join()  # Ждём, пока поток чтения корректно завершится.
    print("Вы вышли из чата.")


if __name__ == "__main__":
    main()
