import socket
import threading


def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if message:
                print(f"\n{message}\nВаше сообщение: ", end="")
            else:
                print("\n[*] Соединение с сервером разорвано.")
                break
        except (ConnectionResetError, BrokenPipeError):
            print("\n[*] Потеряно соединение с сервером.")
            break
        except OSError:
            break


def start_client(host='localhost', port=12345):

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))
        print(f"[*] Подключено к серверу {host}:{port}")
        print("[*] Для выхода введите 'exit'")

        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.daemon = True
        receive_thread.start()

        while True:
            message = input("Ваше сообщение: ")
            if message.lower() == 'exit':
                print("[*] Отключение от сервера...")
                break
            client_socket.send(message.encode('utf-8'))

    except ConnectionRefusedError:
        print(f"[-] Не удалось подключиться к серверу {host}:{port}")
    except KeyboardInterrupt:
        print("\n[*] Принудительное отключение...")
    finally:
        client_socket.close()


if __name__ == "__main__":
    start_client()