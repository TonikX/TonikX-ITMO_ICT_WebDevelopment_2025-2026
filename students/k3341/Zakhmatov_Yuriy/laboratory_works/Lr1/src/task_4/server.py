import socket
import threading

HOST = 'localhost'
PORT = 8080


class ChatServer:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.clients = [] # Кто подключен
        self.nicknames = [] # Никнеймы
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def broadcast(self, message, sender_client=None):
        """Отправка сообщения всем клиентам кроме отправителя"""
        for client in self.clients:
            if client != sender_client:
                try:
                    client.send(message)
                except:
                    # Если отправка не удалась, удаляем клиента
                    self.remove_client(client)

    def remove_client(self, client):
        """Удаление клиента из чата"""
        if client in self.clients:
            index = self.clients.index(client)
            self.clients.remove(client)
            nickname = self.nicknames[index]
            self.nicknames.remove(nickname)

            broadcast_message = f"{nickname} покинул чат!".encode('utf-8')
            self.broadcast(broadcast_message)
            print(f"{nickname} отключился")

    def handle_client(self, client):
        """Обработка сообщений от клиента"""
        while True:
            try:
                message = client.recv(1024)
                if message:
                    self.broadcast(message, client)
                else:
                    self.remove_client(client)
                    break
            except:
                self.remove_client(client)
                break

    def start_server(self):
        """Запуск сервера"""
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Сервер чата запущен на {self.host}:{self.port}")

        while True:
            client, address = self.server_socket.accept()
            print(f"Новое подключение от {str(address)}")

            # Запрос ника у клиента
            client.send("NICK".encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')

            self.nicknames.append(nickname)
            self.clients.append(client)

            print(f"Никнейм клиента: {nickname}")
            broadcast_message = f"{nickname} присоединился к чату!".encode('utf-8')
            self.broadcast(broadcast_message)
            client.send("Подключение к серверу успешно!".encode('utf-8'))

            # Запуск потока для обработки клиента
            thread = threading.Thread(target=self.handle_client, args=(client,), daemon=True)
            thread.start()


if __name__ == "__main__":
    server = ChatServer()
    server.start_server()
