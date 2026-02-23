import socket
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Разрешаем повторное использование адреса (для быстрого перезапуска сервера)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind(('localhost', 1234))
server_socket.listen(5)


client_sockets = set() # Множество для хранения всех подключенных клиентских сокетов
client_sockets_lock = threading.Lock() # Блокировка для безопасного доступа к множеству клиентов из разных потоков


def listen_client(client_socket):#Функция для обработки сообщений от конкретного клиента вызывается в отдельном потоке для каждого клиента

    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')# Получаем сообщение от клиента

            if not message:# Если сообщение пустое, клиент отключился
                break

            print(f"Получено сообщение: {message}")

            with client_sockets_lock:
                clients_copy = client_sockets.copy()

            for other_client in clients_copy: # Рассылаем сообщение всем остальным клиентам
                if other_client != client_socket:  # Не отправляем обратно отправителю
                    try:
                        other_client.send(message.encode('utf-8'))
                    except Exception as e:# Если отправка не удалась, клиент вероятно отключился
                        print(f"Ошибка отправки клиенту: {e}")
                        with client_sockets_lock:
                            client_sockets.discard(other_client)

    except Exception as e:
        print(f"Ошибка при работе с клиентом: {e}")
    finally:# При отключении клиента удаляем его из множества и закрываем соединение
        with client_sockets_lock:
            if client_socket in client_sockets:
                client_sockets.discard(client_socket)
        leave_msg = f"Пользователь покинул чат. Осталось пользователей: {len(client_sockets)}"
        print(leave_msg)
        broadcast_message(leave_msg)
        try:
            client_socket.close()
        except:
            pass

        print(f"Клиент отключен. Всего клиентов: {len(client_sockets)}")


def broadcast_message(message, sender_socket=None):#Функция для рассылки сообщения всем подключенным клиентам
    with client_sockets_lock:
        clients_copy = client_sockets.copy()

    for client in clients_copy:
        if client != sender_socket:  # Не отправляем сообщение отправителю
            try:
                client.send(message.encode('utf-8'))
            except:# Если отправка не удалась, удаляем клиента
                with client_sockets_lock:
                    client_sockets.discard(client)


print("Сервер чата запущен на localhost:1234")
print("Ожидаем подключения клиентов...")
print("Для остановки сервера нажмите Ctrl+C\n")

try:
    while True:
        client_socket, client_address = server_socket.accept()
        print(f'Новый клиент подключился: {client_address}')

        with client_sockets_lock:# Добавляем клиента в множество
            client_sockets.add(client_socket)

        client_thread = threading.Thread(target=listen_client,args=(client_socket,))# Создаем и запускаем поток для обработки клиента
        client_thread.daemon = True # Делаем поток демоном (завершится при завершении основного потока)
        client_thread.start()

        welcome_msg = "Добро пожаловать в чат! Вы подключились к серверу."# Отправляем приветственное сообщение новому клиенту
        client_socket.send(welcome_msg.encode('utf-8'))

        join_msg = f"Новый пользователь присоединился к чату. Всего пользователей: {len(client_sockets)}"# Уведомляем всех о новом подключении
        broadcast_message(join_msg, client_socket)

except KeyboardInterrupt:
    # Обрабатываем прерывание Ctrl+C для корректного завершения
    print("\nОстанавливаем сервер...")
finally:
    print("Закрываем все соединения...")# Корректно закрываем все соединения при завершении работы

    with client_sockets_lock:# Закрываем все клиентские сокеты
        for client_socket in client_sockets:
            try:
                client_socket.close()
            except:
                pass
        client_sockets.clear()

    server_socket.close()
    print("Сервер остановлен.")



