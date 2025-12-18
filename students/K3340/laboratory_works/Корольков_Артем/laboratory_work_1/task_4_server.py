import socket
import threading


class ChatServer:
    def __init__(self, host='localhost', port=12347):
        self.host = host
        self.port = port
        self.clients = []  # Список подключенных клиентов
        self.nicknames = []  # Список никнеймов
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.lock = threading.Lock()  # Блокировка для потокобезопасности

    def broadcast(self, message, sender_client=None):
        """Отправляет сообщение всем подключенным клиентам, кроме отправителя"""
        with self.lock:
            for client in self.clients:
                if client != sender_client:
                    try:
                        client.send(message)
                    except:
                        # Если отправка не удалась, удаляем клиента
                        self.remove_client(client)

    def remove_client(self, client):
        """Удаляет клиента из списка подключенных"""
        if client in self.clients:
            index = self.clients.index(client)
            self.clients.remove(client)
            nickname = self.nicknames[index]
            self.nicknames.remove(nickname)
            self.broadcast(f'{nickname} покинул чат!'.encode('utf-8'))
            client.close()

    def handle_client(self, client):
        """Обрабатывает сообщения от клиента"""
        while True:
            try:
                message = client.recv(1024)
                if message:
                    self.broadcast(message, client)
                else:
                    # Пустое сообщение означает отключение клиента
                    self.remove_client(client)
                    break
            except:
                self.remove_client(client)
                break

    def receive_connections(self):
        """Принимает новые подключения"""
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Сервер чата запущен на {self.host}:{self.port}")
        print("Ожидание подключений...")

        while True:
            client, address = self.server_socket.accept()
            print(f"Подключился клиент с адресом: {address}")

            # Запрашиваем никнейм у клиента
            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')

            with self.lock:
                self.nicknames.append(nickname)
                self.clients.append(client)

            print(f'Никнейм клиента: {nickname}')
            self.broadcast(f'{nickname} присоединился к чату!'.encode('utf-8'))
            client.send('Подключение к серверу успешно!'.encode('utf-8'))

            # Запускаем поток для обработки сообщений клиента
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.daemon = True  # Поток завершится при завершении основной программы
            thread.start()

    def start(self):
        """Запускает сервер"""
        try:
            self.receive_connections()
        except KeyboardInterrupt:
            print("\nОстановка сервера...")
        finally:
            self.server_socket.close()


if __name__ == "__main__":
    server = ChatServer()
    server.start()