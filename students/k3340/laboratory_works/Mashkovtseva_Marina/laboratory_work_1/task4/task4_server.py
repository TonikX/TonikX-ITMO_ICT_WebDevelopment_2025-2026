import socket
import threading

# Настройки сервера
HOST = 'localhost'
PORT = 8080

# Создаем TCP-сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Чат-сервер запущен на {HOST}:{PORT}...")

# Список для хранения всех подключенных клиентов
clients = []


def handle_client(client):
    """Обрабатывает сообщения от конкретного клиента"""
    while True:
        try:
            # Получаем сообщение от клиента
            message = client.recv(1024).decode('utf-8')

            if message:
                # Рассылаем сообщение всем клиентам
                for client_item in clients:
                    if client_item != client:  # Не отправляем отправителю
                        client_item.send(message.encode('utf-8'))
            else:
                # Пустое сообщение = отключение
                break

        except:
            # Ошибка при получении = отключение
            break

    # Удаляем клиента при отключении
    if client in clients:
        clients.remove(client)
    client.close()


# Принимаем новые подключения
while True:
    # Принимаем новое подключение
    client_connection, client_address = server_socket.accept()
    print(f"Новое подключение от {client_address}")

    # Добавляем клиента в список
    clients.append(client_connection)

    # Создаем поток для общения с этим клиентом
    client_thread = threading.Thread(target=handle_client, args=(client_connection,))
    client_thread.daemon = True # Делаем поток фоновым (завершится вместе с сервером)
    client_thread.start() # Запускаем поток