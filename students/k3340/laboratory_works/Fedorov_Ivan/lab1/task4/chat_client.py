import socket
import threading
import time
import sys


class ChatClient:
    def __init__(self, host='localhost', port=5050):
        self.host = host
        self.port = port
        self.socket = None
        self.username = None
        self.running = False

    def receive_messages(self):
        """Поток для получения сообщений от сервера"""
        while self.running:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if not message:
                    print("\nСоединение с сервером разорвано")
                    break
                print(f"\r{message}\n[Вы]: ", end="")
            except:
                break

    def send_message(self, message):
        """Отправляет сообщение на сервер"""
        try:
            self.socket.send(message.encode('utf-8'))
            return True
        except:
            return False

    def connect(self):
        """Подключается к серверу"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            return True
        except:
            print(f"Не удалось подключиться к серверу {self.host}:{self.port}")
            return False

    def start(self):
        """Запускает клиент"""
        print("=" * 50)
        print("МНОГОПОЛЬЗОВАТЕЛЬСКИЙ ЧАТ КЛИЕНТ")
        print("=" * 50)

        # Подключаемся к серверу
        if not self.connect():
            return

        # Получаем имя пользователя
        self.username = input("Введите ваше имя: ").strip()
        while not self.username:
            self.username = input("Имя не может быть пустым. Введите ваше имя: ").strip()

        # Отправляем имя на сервер
        if not self.send_message(self.username):
            print("Ошибка при отправке имени")
            return

        self.running = True

        # Запускаем поток для получения сообщений
        receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        receive_thread.start()

        print("\n" + "=" * 50)
        print(f"Добро пожаловать в чат, {self.username}!")
        print("Команды:")
        print("  /quit - выйти из чата")
        print("  /users - показать участников онлайн")
        print("=" * 50)
        print()

        # Основной цикл отправки сообщений
        try:
            while self.running:
                message = input("[Вы]: ").strip()

                if not message:
                    continue

                if message.lower() == '/quit':
                    self.send_message('/quit')
                    break
                elif message.lower() == '/users':
                    print("Информация о пользователях недоступна в этой версии")
                else:
                    if not self.send_message(message):
                        print("Ошибка отправки сообщения")
                        break

        except KeyboardInterrupt:
            print("\nВыход из чата...")
        finally:
            self.running = False
            if self.socket:
                self.socket.close()
            print("Чат завершен")


if __name__ == "__main__":
    client = ChatClient()
    client.start()