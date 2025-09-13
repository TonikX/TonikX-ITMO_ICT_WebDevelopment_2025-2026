import socket
import threading
from utils import server_address


def receive_messages(client_socket):
    """Функция для получения сообщений от сервера"""
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


def send_messages(client_socket, nickname):
    """Функция для отправки сообщений серверу"""
    while True:
        message_text = input()
        message = f'{nickname}: {message_text}'
        client_socket.send(message.encode('utf-8'))


def start_client():
    """Функция для создания TCP сокета клиента, отправки сообщений серверу
    и обработки ответов"""
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
