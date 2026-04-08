import socket
import threading

# Список всех подключённых клиентов
clients = []
# Словарь для хранения имени каждого клиента по его сокету
client_names = {}
# Счётчик клиентов для генерации временных имён
client_count = 0
# Флаг работы сервера
running = True

# Функция для рассылки сообщения всем клиентам, кроме отправителя
def broadcast(message, sender_socket=None):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                continue  # Игнорируем ошибки при отправке

# Функция для обработки сообщений от одного клиента
def handle_client(client_socket):
    name = client_names[client_socket]
    client_socket.settimeout(1.0)  # Тайм-аут для возможности проверки флага running
    while running:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                full_message = f"{name}: {message}"
                print(full_message)
                broadcast(full_message, sender_socket=client_socket)
            else:
                break  # Клиент отключился
        except socket.timeout:
            continue  # Проверяем running снова
        except:
            break

    # После выхода из цикла: удаляем клиента и уведомляем других
    if client_socket in clients:
        clients.remove(client_socket)
    if client_socket in client_names:
        del client_names[client_socket]
    client_socket.close()
    
    exit_message = f"{name} покинул чат."
    broadcast(exit_message)
    print(exit_message)

# Основная функция сервера
def start_server():
    global client_count, running
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5555))
    server_socket.listen(5)
    server_socket.settimeout(1.0)  # Тайм-аут для проверки флага running
    print("Сервер запущен и слушает порт 5555...")

    try:
        while running:
            try:
                client_socket, client_address = server_socket.accept()
            except socket.timeout:
                continue  # Проверяем флаг running снова
            client_count += 1
            client_name = f"Client{client_count}"
            client_names[client_socket] = client_name
            clients.append(client_socket)
            print(f"{client_name} подключился с адреса {client_address}")
            
            # Создаём отдельный поток для обслуживания клиента
            thread = threading.Thread(target=handle_client, args=(client_socket,), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        print("\nОстановка сервера по Ctrl+C...")
        running = False
        # Закрываем все клиентские соединения
        for client in clients:
            client.close()
        server_socket.close()
        print("Сервер остановлен.")

# Запуск сервера
if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("\nСервер остановлен пользователем.")
