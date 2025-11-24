import socket
import threading
from dataclasses import dataclass


class Config:
    HOST = "localhost"
    PORT = 8004
    BUFFER_SIZE = 1024


@dataclass
class ClientInfo:
    socket: socket.socket
    nickname: str
    running: bool = True


client_info: ClientInfo | None = None


def receive_messages() -> None:
    while client_info and client_info.running:
        try:
            message = client_info.socket.recv(Config.BUFFER_SIZE).decode("utf-8")
            if not message:
                break
            print(message)
        except Exception:
            break


def send_messages() -> None:
    print("Введите сообщения (для выхода введите exit):")

    while client_info and client_info.running:
        try:
            message = input()
            if message.lower() == "exit":
                client_info.running = False
                client_info.socket.send(message.encode("utf-8"))
                break

            if not message.strip():
                continue

            client_info.socket.send(message.encode("utf-8"))
        except Exception:
            break


def client_to_thread(client_socket: socket.socket) -> None:
    global client_info

    nickname = input("Введите ваш никнейм: ").strip() or "Аноним"
    client_socket.send(nickname.encode("utf-8"))

    client_info = ClientInfo(client_socket, nickname)

    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.daemon = True
    receive_thread.start()

    send_messages()


def run_client() -> None:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((Config.HOST, Config.PORT))
        print(f"Подключение к серверу {Config.HOST}:{Config.PORT}")

        client_to_thread(client_socket)

    except ConnectionRefusedError:
        print("Не удалось подключиться к серверу. Проверьте, что сервер запущен.")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        if client_info:
            client_info.running = False
        client_socket.close()
        print("Отключение от сервера")


if __name__ == "__main__":
    run_client()
