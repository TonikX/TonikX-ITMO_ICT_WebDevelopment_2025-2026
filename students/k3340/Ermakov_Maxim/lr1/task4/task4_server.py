# server.py
import socket
import threading

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9092

# Общий список всех подключенных клиентов.
# Каждый элемент: словарь с ключами {"socket", "file", "name"}.
connected_clients = []
connected_clients_lock = threading.Lock()


def broadcast_message(text_message):
    # Отправляет сообщение всем подключенным пользователям.
    with connected_clients_lock:
        for client in connected_clients:
            try:
                client["socket"].sendall((text_message + "\n").encode("utf-8"))
            except Exception:
                # Если не удалось отправить, просто пропускаем (пользователь, вероятно, отвалился)
                pass


def handle_client_connection(client_socket, client_address):
    """
    Обрабатывает одного клиента в отдельном потоке:
    - читает имя пользователя (первая строка);
    - принимает сообщения строками и рассылает их всем;
    - удаляет клиента при отключении.
    """

    client_file = client_socket.makefile("r", encoding="utf-8", newline="\n")

    try:
        # 1) Первая строка — имя пользователя
        user_name = client_file.readline()
        if not user_name:
            client_socket.close()
            return
        user_name = user_name.strip()

        # 2) Сохраняем клиента в общий список
        with connected_clients_lock:
            connected_clients.append({"socket": client_socket, "file": client_file, "name": user_name})

        print(f"Подключился пользователь: {user_name} с адреса {client_address}")
        broadcast_message(f"[СИСТЕМА] Пользователь {user_name} вошёл в чат.")

        # 3) Основной цикл приёма сообщений
        while True:
            line = client_file.readline()
            if not line:
                # Клиент закрыл соединение
                break
            text_message = line.rstrip("\n")
            # Пустые строки игнорируем
            if text_message.strip() == "":
                continue

            # Рассылаем всем
            broadcast_message(f"{user_name}: {text_message}")

    except Exception as error:
        print(f"Ошибка для клиента {client_address}: {error}")

    finally:
        # Удаляем клиента из списка и закрываем соединение
        with connected_clients_lock:
            for client in list(connected_clients):
                if client["socket"] is client_socket:
                    connected_clients.remove(client)
                    break

        try:
            client_file.close()
        except Exception:
            pass
        try:
            client_socket.close()
        except Exception:
            pass

        print(f"Пользователь {client_address} отключился.")
        broadcast_message(f"[СИСТЕМА] Пользователь {user_name} покинул чат.")


def main():
    # Создаём TCP-серверный сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Чтобы можно было быстро перезапускать сервер на том же порту
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(10)

    print(f"Чат-сервер запущен на {SERVER_HOST}:{SERVER_PORT}")
    print("Ожидаю подключения клиентов...\n")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            # Для каждого клиента запускаем отдельный поток
            client_thread = threading.Thread(
                target=handle_client_connection,
                args=(client_socket, client_address),
                daemon=True
            )
            client_thread.start()
    except KeyboardInterrupt:
        print("\nСервер остановлен пользователем.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
