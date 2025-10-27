# Задание 4: Многопользовательский чат
## Описание задания
Реализовать многопользовательский чат с использованием потоков. Сервер должен поддерживать одновременное подключение нескольких клиентов и обеспечивать обмен сообщениями между ними.

## Ход выполнения
### Серверная часть (task_4_server.py):
```python
import socket
import threading

class ChatServer:
    def __init__(self, host='localhost', port=12347):
        self.host = host
        self.port = port
        self.clients = []
        self.nicknames = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.lock = threading.Lock()

    def broadcast(self, message, sender_client=None):
        with self.lock:
            for client in self.clients:
                if client != sender_client:
                    try:
                        client.send(message)
                    except:
                        self.remove_client(client)

    def remove_client(self, client):
        if client in self.clients:
            index = self.clients.index(client)
            self.clients.remove(client)
            nickname = self.nicknames[index]
            self.nicknames.remove(nickname)
            self.broadcast(f'{nickname} покинул чат!'.encode('utf-8'))
            client.close()

    def handle_client(self, client):
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

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Сервер чата запущен на {self.host}:{self.port}")
        
        while True:
            client, address = self.server_socket.accept()
            print(f"Подключился клиент с адресом: {address}")
            
            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            
            with self.lock:
                self.nicknames.append(nickname)
                self.clients.append(client)
            
            print(f'Никнейм клиента: {nickname}')
            self.broadcast(f'{nickname} присоединился к чату!'.encode('utf-8'))
            client.send('Подключение к серверу успешно!'.encode('utf-8'))
            
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.daemon = True
            thread.start()
```
### Клиентская часть (task_4_client.py):
```python
import socket
import threading

class ChatClient:
    def __init__(self, host='localhost', port=12347):
        self.host = host
        self.port = port
        self.nickname = input("Введите ваш никнейм: ")
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.client_socket.send(self.nickname.encode('utf-8'))
                else:
                    print(message)
            except:
                print("Произошла ошибка при получении сообщения!")
                self.client_socket.close()
                break

    def send_messages(self):
        while True:
            message = input()
            if message.lower() == 'quit':
                self.client_socket.close()
                break
            formatted_message = f'{self.nickname}: {message}'
            self.client_socket.send(formatted_message.encode('utf-8'))

    def start(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print("Подключение к чату установлено!")
            
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            self.send_messages()
        except Exception as e:
            print(f"Ошибка подключения: {e}")
        finally:
            self.client_socket.close()
```
## Вывод по заданию 4
Реализован полнофункциональный многопользовательский чат с поддержкой одновременного подключения нескольких клиентов. Использование потоков позволяет эффективно обрабатывать сообщения от разных пользователей. Сервер корректно управляет подключениями и обеспечивает широковещательную рассылку сообщений.
