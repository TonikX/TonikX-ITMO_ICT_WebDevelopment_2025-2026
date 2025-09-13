import socket
import threading
from utils import server_address

clients = []  # Список для хранения сокетов всех клиентов


def broadcast(message, sender_connection):
    """Функция для рассылки сообщений всем клиентам, кроме отправителя"""
    for client_conn in clients:
        try:
            if sender_connection is not client_conn:
                client_conn.send(message)
        except:
            # Если отправка не удалась, клиент отключился
            clients.remove(client_conn)
            client_conn.close()


def handle_client(connection, address):
    """Функция для обработки сообщений от клиента"""
    print(f'[НОВОЕ ПОДКЛЮЧЕНИЕ] {address} подключился.')

    while True:
        try:
            # Получаем сообщение
            message = connection.recv(1024)
            if message:
                print(f'[{address}] {message.decode("utf-8")}')
                # Рассылаем его всем остальным
                broadcast(message, connection)
            else:
                # Если сообщение пустое, клиент отключился
                print(f'[{address}] отключился.')
                clients.remove(connection)
                connection.close()
                break
        except:
            print(f'[{address}] соединение разорвано.')
            clients.remove(connection)
            connection.close()
            break


# Основная часть сервера
def start_server():
    """Функция для создания TCP сокета сервера, к которому происходит подключение,
    и запуска обработки новых клиентов в отдельных потоках"""
    # Создаем TCP сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    print(f'Сервер запущен на {server_address[0]}:{server_address[1]}')

    server_socket.listen(1)

    while True:
        # Принимаем новое подключение
        connection, address = server_socket.accept()
        # Добавляем нового клиента в список
        clients.append(connection)
        # Создаем и запускаем для него новый поток
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()
        print(f'[АКТИВНЫЕ ПОДКЛЮЧЕНИЯ] {threading.active_count() - 1}')


if __name__ == "__main__":
    start_server()
