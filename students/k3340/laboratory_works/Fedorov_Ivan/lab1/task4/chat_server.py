import socket
import threading
import time
from datetime import datetime


class ChatServer:
    def __init__(self, host='localhost', port=5050):
        self.host = host
        self.port = port
        self.clients = {}  # {socket: {'username': 'name', 'address': addr}}
        self.server_socket = None
        self.running = False

    def broadcast(self, message, sender_socket=None):
        """Отправляет сообщение всем клиентам, кроме отправителя"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"

        disconnected_clients = []

        for client_socket, client_info in self.clients.items():
            try:
                if client_socket != sender_socket:
                    client_socket.send(formatted_message.encode('utf-8'))
            except:
                disconnected_clients.append(client_socket)

        # Удаляем отключенных клиентов
        for client in disconnected_clients:
            self.remove_client(client)

    def remove_client(self, client_socket):
        """Удаляет клиента из списка"""
        if client_socket in self.clients:
            username = self.clients[client_socket]['username']
            self.clients.pop(client_socket)
            try:
                client_socket.close()
            except:
                pass

            # Уведомляем других пользователей
            leave_message = f"⚡ {username} покинул(а) чат"
            self.broadcast(leave_message)
            print(f"Клиент отключен: {username}")

    def handle_client(self, client_socket, client_address):
        """Обрабатывает сообщения от клиента"""
        try:
            # Получаем имя пользователя
            username = client_socket.recv(1024).decode('utf-8').strip()

            if not username:
                client_socket.close()
                return

            # Сохраняем информацию о клиенте
            self.clients[client_socket] = {
                'username': username,
                'address': client_address
            }

            # Уведомляем о новом пользователе
            join_message = f"🎉 {username} присоединился(ась) к чату!"
            self.broadcast(join_message)
            print(f"Новый пользователь: {username} ({client_address})")

            # Отправляем приветственное сообщение
            welcome_msg = f"[Сервер] Добро пожаловать в чат, {username}! Участников онлайн: {len(self.clients)}"
            client_socket.send(welcome_msg.encode('utf-8'))

            # Основной цикл обработки сообщений
            while self.running:
                try:
                    message = client_socket.recv(1024).decode('utf-8')

                    if not message:
                        break

                    if message.strip().lower() == '/quit':
                        break

                    # Транслируем сообщение всем
                    chat_message = f"{username}: {message}"
                    self.broadcast(chat_message, client_socket)
                    print(f"Сообщение от {username}: {message}")

                except ConnectionResetError:
                    break
                except Exception as e:
                    print(f"Ошибка при получении сообщения от {username}: {e}")
                    break

        except Exception as e:
            print(f"Ошибка обработки клиента {client_address}: {e}")
        finally:
            self.remove_client(client_socket)

    def get_server_info(self):
        """Возвращает информацию о сервере"""
        return f"Сервер чата запущен на {self.host}:{self.port}\nУчастников онлайн: {len(self.clients)}"

    def start(self):
        """Запускает сервер"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True

            print("=" * 50)
            print("МНОГОПОЛЬЗОВАТЕЛЬСКИЙ ЧАТ СЕРВЕР")
            print("=" * 50)
            print(f"Сервер запущен на {self.host}:{self.port}")
            print("Ожидание подключений...")
            print("Для остановки сервера нажмите Ctrl+C")
            print("=" * 50)

            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()

                    # Запускаем поток для обработки клиента
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address),
                        daemon=True
                    )
                    client_thread.start()

                    print(f"Новое подключение от {client_address}")

                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"Ошибка при принятии подключения: {e}")

        except KeyboardInterrupt:
            print("\nОстановка сервера...")
        except Exception as e:
            print(f"Ошибка сервера: {e}")
        finally:
            self.running = False
            if self.server_socket:
                self.server_socket.close()
            print("Сервер остановлен")


if __name__ == "__main__":
    server = ChatServer()
    server.start()