import socket
import threading
import sys

# Настройки сервера
HOST = '127.0.0.1'  # Локальный адрес
PORT = 55555  # Выбранный порт
# Список для хранения всех подключенных клиентов (сокетов)
clients = []
# Блокировка для обеспечения безопасности при работе с общим списком клиентов
lock = threading.Lock()


def broadcast(message, sender_socket=None):
    """Отправляет сообщение всем подключенным клиентам, кроме отправителя (по желанию)."""
    with lock:
        # Проходим по копии списка, чтобы избежать проблем, если клиент отключится во время цикла
        for client in clients:
            if client != sender_socket:
                try:
                    client.send(message)
                except:
                    # Если отправка не удалась, значит, клиент отключился
                    client.close()
                    # Удаляем "мертвый" сокет из списка
                    if client in clients:
                        clients.remove(client)


def handle_client(client_socket, client_address):
    """Функция, которая запускается в отдельном потоке для каждого клиента."""
    print(f"[НОВОЕ] Соединение установлено: {client_address}")

    # 1. Получаем никнейм клиента
    try:
        nickname = client_socket.recv(1024).decode('utf-8')
        print(f"[НИК] Клиент {client_address} представился как: {nickname}")

        # Уведомляем всех о подключении нового пользователя
        join_message = f"[СЕРВЕР] {nickname} присоединился к чату!".encode('utf-8')
        broadcast(join_message, client_socket)

    except:
        # Если не удалось получить никнейм, закрываем соединение
        client_socket.close()
        with lock:
            if client_socket in clients:
                clients.remove(client_socket)
        return

    while True:
        try:
            # Получаем сообщение от клиента
            message = client_socket.recv(1024)
            if message:
                # Формируем сообщение для рассылки: "Никнейм: Сообщение"
                full_message = f"[{nickname}] {message.decode('utf-8')}".encode('utf-8')
                print(f"[РАССЫЛКА] {full_message.decode('utf-8')}")
                broadcast(full_message, client_socket)
            else:
                # Если сообщение пустое, клиент отключился
                raise Exception("Клиент отключился")

        except:
            # Обработка отключения клиента
            print(f"[ОТКЛЮЧЕНИЕ] Клиент {nickname} ({client_address}) отключился.")

            with lock:
                if client_socket in clients:
                    clients.remove(client_socket)

            # Уведомляем всех об отключении
            leave_message = f"[СЕРВЕР] {nickname} покинул чат.".encode('utf-8')
            broadcast(leave_message)
            client_socket.close()
            break  # Выход из цикла while True


def start_server():
    """Инициализация и запуск TCP-сервера."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Позволяет повторно использовать адрес сразу после завершения работы
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((HOST, PORT))
        server.listen()
    except Exception as e:
        print(f"Не удалось запустить сервер: {e}")
        sys.exit()

    print(f"Чат-сервер запущен на {HOST}:{PORT}. Ожидание подключений...")

    try:
        while True:
            # Ожидание нового соединения
            client_socket, client_address = server.accept()

            # Добавляем новый сокет в список клиентов
            with lock:
                clients.append(client_socket)

            # Запускаем новый поток для обработки этого клиента
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            thread.start()

            # Выводим количество активных потоков (клиентов)
            print(f"[АКТИВНО] Текущее количество подключений: {threading.active_count() - 1}")

    except KeyboardInterrupt:
        print("\nСервер остановлен. Закрытие всех соединений.")
    except Exception as e:
        print(f"Общая ошибка сервера: {e}")

    finally:
        server.close()
        print("Серверный сокет закрыт.")


if __name__ == "__main__":
    start_server()