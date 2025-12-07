import socket
import threading
from typing import Tuple, Dict


# клиент == пользователь

# Храним подключённые сокеты (пользователей)
clients: Dict[socket.socket, str] = {} # сокет: никнейм
# блокировка, чтобы не было race condition
clients_lock = threading.Lock()


def broadcast(message: str) -> None:
    '''
    Отправляет сообщение всем пользователям
    message: сообщение в байтах
    sender_socket: сокет, откуда пришло сообщение
    '''
    with clients_lock:
        for client in list(clients):
            # Отправляем сообщение всем
            try:
                client.send(message.encode('utf-8'))
            except Exception:
                # Предполагаем, что если невозможно отправить пользователю сообщение,
                # то он отключился от сервера, удаляем его сокет
                client.close()
                del clients[client]


def handle_client(client_socket: socket.socket, client_address: Tuple[str, int]) -> None:
    '''
    Обработчик для каждого пользователям в отдельном потоке
    Получает сообщение от пользователям и рассылает всем остальным пользователям
    client_socket: клиентский сокет
    client_address: пара (IP, порт)
    '''
    nickname = client_socket.recv(1024).decode('utf-8').strip()
    # Добавили нового пользователя в список подключённых пользователей
    with clients_lock:
        clients[client_socket] = nickname
    print(f'[Сервер]: {nickname} присоединился к чату')

    while True:
        try:
            msg = client_socket.recv(1024)
            if not msg:
                print(f'Пользователь [{client_address}/{nickname}] отключился от чата')
                broadcast(f'[Сервер]: {nickname} покинул чат')
                break

            message_text = msg.decode('utf-8')
            # Вывод сообщение в консоль сервера
            print(f'{nickname}: {message_text}')

            # Отправляем сообщение всем остальным клиентам
            broadcast(f'{nickname}: {message_text}')

        except ConnectionResetError:
            # Если соединение было оборвано
            print(f'{client_address} вылетел')
            break
        except Exception as e:
            print(f'Ошибка при работе с {client_address}: {e}')

    # После выхода из цикла завершаем удаляем пользователя из списка и
    # заверщаем сессию пользователя
    with clients_lock:
        if client_socket in clients:
            del clients[client_socket]
    client_socket.close()


def run_server(server_host: str = 'localhost', server_port: int = 8080) -> None:
    '''
    Запускает сервер чата
    host: IP-адрес для привязки сервера
    port: порт для прослушивания
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((server_host, server_port))
        server.listen(5)
        print(f'Сервер чата запущен на {server_host}:{server_port}')

        while True:
            client_socket, client_address = server.accept()

            # Запускаем поток
            thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address),
                daemon=True
            )
            thread.start()


if __name__ == '__main__':
    run_server()
