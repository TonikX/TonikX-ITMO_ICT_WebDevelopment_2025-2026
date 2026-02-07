# chat_client.py
import socket
import threading
import sys

def receive_messages(client_socket):
    """Получает и выводит входящие сообщения"""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except ConnectionResetError:
            print("[!] Соединение с сервером потеряно.")
            break
        except OSError:
            break  # Сокет закрыт


def main():
    HOST = 'localhost'
    PORT = 12345

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
        print("[*] Подключено к чату. Введите своё имя:")
        username = input().strip()
        if not username:
            username = "Anonymous"

        # Запускаем поток для получения сообщений
        recv_thread = threading.Thread(target=receive_messages, args=(client,))
        recv_thread.daemon = True
        recv_thread.start()

        print(f"[+] Привет, {username}! Вводите сообщения (Ctrl+C или exit для выхода):")

        while True:
            try:
                msg = input()
                if msg.lower() == 'exit':
                    break
                full_message = f"{username}: {msg}"
                client.send(full_message.encode('utf-8'))
            except KeyboardInterrupt:
                break

    except ConnectionRefusedError:
        print("[!] Не удалось подключиться к серверу.")
    finally:
        client.close()
        print("[*] Отключено.")


if __name__ == "__main__":
    main()