import socket
import threading

# Список всех подключенных клиентов
clients = []
# Словарь для хранения никнеймов клиентов
nicknames = {}

def broadcast_message(message, sender_client=None):
    """Отправляет сообщение всем подключенным клиентам"""
    print(f"Рассылка сообщения: {message.strip()}", flush=True)
    
    # Список клиентов для удаления (если отключились)
    clients_to_remove = []
    
    for client in clients:
        if client != sender_client:  # Не отправляем отправителю
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                # Клиент отключился
                print(f"Ошибка отправки клиенту: {e}", flush=True)
                clients_to_remove.append(client)
    
    # Удаляем отключившихся клиентов
    for client in clients_to_remove:
        remove_client(client)

def remove_client(client):
    """Удаляет клиента из списков"""
    if client in clients:
        clients.remove(client)
    
    if client in nicknames:
        nickname = nicknames[client]
        print(f"Пользователь {nickname} отключился")
        
        # Уведомляем других о том, что пользователь покинул чат
        leave_message = f"*** {nickname} покинул чат ***\n"
        broadcast_message(leave_message)
        
        del nicknames[client]

def handle_client(client, address):
    """Обрабатывает сообщения от конкретного клиента"""
    try:
        # Запрашиваем никнейм
        client.send("Введите ваш никнейм: ".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8').strip()
        
        # Сохраняем никнейм
        nicknames[client] = nickname
        print(f"Пользователь {nickname} подключился с адреса {address}")
        
        # Приветствуем нового пользователя
        welcome_message = f"Добро пожаловать в чат, {nickname}!\n"
        client.send(welcome_message.encode('utf-8'))
        
        # Уведомляем всех о новом пользователе
        join_message = f"*** {nickname} присоединился к чату ***\n"
        broadcast_message(join_message, client)
        
        # Основной цикл обработки сообщений
        while True:
            message = client.recv(1024).decode('utf-8')
            
            if not message:
                break
                
            # Убираем лишние символы и проверяем на пустоту
            clean_message = message.strip()
            if not clean_message:
                continue
                
            # Формируем сообщение с никнеймом отправителя
            formatted_message = f"{nickname}: {clean_message}\n"
            print(f"Сообщение от {nickname}: {clean_message}")
            
            # Рассылаем всем остальным клиентам
            broadcast_message(formatted_message, client)
            
    except Exception as e:
        print(f"Ошибка при обработке клиента {address}: {e}")
    finally:
        # Удаляем клиента при отключении
        remove_client(client)
        client.close()

def start_server():
    """Запускает сервер чата"""
    # Создаем TCP сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Настройки сервера
    host = 'localhost'
    port = 12347
    
    server_socket.bind((host, port))
    server_socket.listen(10)  # Поддерживаем до 10 подключений в очереди
    
    print(f"🚀 Сервер чата запущен на {host}:{port}")
    print("Ожидание подключений...")
    
    try:
        while True:
            # Принимаем новое подключение
            client_socket, client_address = server_socket.accept()
            clients.append(client_socket)
            
            print(f"Новое подключение от {client_address}")
            
            # Создаем новый поток для обработки клиента
            client_thread = threading.Thread(
                target=handle_client, 
                args=(client_socket, client_address)
            )
            client_thread.daemon = True  # Поток завершится при завершении программы
            client_thread.start()
            
    except KeyboardInterrupt:
        print("\n🛑 Завершение работы сервера...")
    finally:
        # Закрываем все соединения
        for client in clients:
            client.close()
        server_socket.close()
        print("Сервер остановлен.")

if __name__ == "__main__":
    start_server()
