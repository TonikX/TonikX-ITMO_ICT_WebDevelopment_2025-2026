import socket
import threading

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024)
            if not message:
                print("Соединение закрыто сервером.")
                break
            print(message.decode('UTF-8'))
        except (ConnectionResetError, ConnectionAbortedError, OSError) as e:
            print(f"Ошибка соединения: {e}")
            break

def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(('127.0.0.1', 11111))
        # Запускаем отдельный поток для получения и печати входящих сообщений
        threading.Thread(
            target=receive_messages,
            args=(client_socket,),
            daemon=True
        ).start()
        while True:
            try:
                message = input()
                if message:
                    client_socket.send(message.encode('UTF-8'))
            except (ConnectionResetError, ConnectionAbortedError, OSError) as e:
                print(f"Ошибка соединения: {e}")
                break

if __name__ == "__main__":
    run_client()
