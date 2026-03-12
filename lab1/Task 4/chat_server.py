import socket
import threading

HOST = "localhost"  # Адрес сервера
PORT = 8080         # Порт сервера

clients = []                 # Список подключенных клиентов
clients_lock = threading.Lock()  # Блокировка для безопасного доступа к списку клиентов из разных потоков

def broadcast(message, sender_socket=None):
    """Отправить сообщение всем клиентам, кроме отправителя"""
    with clients_lock:  # Защищаем доступ к списку клиентов
        for client in clients[:]:
            if client is not sender_socket:
                try:
                    client.sendall(message.encode("utf-8"))
                except:  # Если отправка не удалась, закрываем соединение
                    client.close()
                    clients.remove(client)

def handle_client(client_socket, addr):
    """Обработка сообщений одного клиента"""
    print(f"[+] Подключился {addr}")
    client_socket.sendall("Добро пожаловать в чат!\n".encode("utf-8"))

    while True:
        try:
            data = client_socket.recv(1024)  # Получаем данные от клиента
            if not data:  # Клиент отключился
                break
            message = data.decode("utf-8").strip()
            print(f"{addr}: {message}")  # Логируем сообщение на сервере
            broadcast(f"{addr}: {message}", sender_socket=client_socket)  # Рассылаем другим клиентам
        except:
            break

    # Удаляем клиента из списка и закрываем соединение
    with clients_lock:
        if client_socket in clients:
            clients.remove(client_socket)
    client_socket.close()
    print(f"[-] {addr} отключился")

# Настройка TCP-сокета сервера
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)  # Разрешаем очередь из 5 ожидающих подключений
print(f"Сервер запущен на {HOST}:{PORT}")

try:
    while True:
        client_socket, addr = server_socket.accept()  # Ждем подключения нового клиента
        with clients_lock:
            clients.append(client_socket)  # Добавляем клиента в список
        # Создаем поток для обслуживания нового клиента
        threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()
except KeyboardInterrupt:
    print("\nВыключение сервера...")
finally:
    # Закрываем все соединения при завершении работы
    with clients_lock:
        for client in clients:
            client.close()
    server_socket.close()
