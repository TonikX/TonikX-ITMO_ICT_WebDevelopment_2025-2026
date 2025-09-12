import socket
import threading
from utils import server_address


# Функция для получения сообщений от сервера
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                break
        except:
            print("Соединение с сервером разорвано.")
            client_socket.close()
            break


# Функция для отправки сообщений серверу
def send_messages(client_socket, nickname):
    while True:
        message_text = input()
        message = f'{nickname}: {message_text}'
        client_socket.send(message.encode('utf-8'))


# Основная часть клиента
def start_client():
    nickname = input("Введите ваш ник: ")
    # Создаем TCP сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)

    # Запускаем поток для получения сообщений
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    # Запускаем отправку сообщений в основном потоке
    send_messages(client_socket, nickname)


if __name__ == "__main__":
    start_client()
