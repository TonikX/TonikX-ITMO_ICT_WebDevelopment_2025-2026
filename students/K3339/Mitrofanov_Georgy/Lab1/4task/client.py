import socket
import threading


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            print(message)
        except:
            print("Соединение разорвано!")
            client_socket.close()
            break


def start_client(host="localhost", port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))

        nickname_request = client_socket.recv(1024).decode("utf-8")
        if nickname_request == "NICK":
            nickname = input("Введите ваш никнейм: ")
            client_socket.send(nickname.encode("utf-8"))

        receive_thread = threading.Thread(
            target=receive_messages, args=(client_socket,)
        )
        receive_thread.daemon = True
        receive_thread.start()

        while True:
            print(f"{nickname} : ", end="")
            message = input()
            if message.lower() == "quit":
                client_socket.close()
                break
            try:
                client_socket.send(message.encode("utf-8"))
            except:
                print("Ошибка отправки сообщения!")
                break

    except Exception as e:
        print(f"Ошибка подключения: {e}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    start_client()
