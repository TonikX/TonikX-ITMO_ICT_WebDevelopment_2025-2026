import socket
import threading


HOST = 'localhost'
PORT = 8080

class ChatClient:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nickname = None

    def receive_messages(self):
        """Получение сообщений от сервера"""
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message == "NICK":
                    self.client_socket.send(self.nickname.encode('utf-8'))
                else:
                    print(message)
            except:
                print("Произошла ошибка!")
                self.client_socket.close()
                break

    def send_messages(self):
        """Отправка сообщений на сервер"""
        while True:
            try:
                message = input()
                if message.lower() == 'exit':
                    break
                formatted_message = f"{self.nickname}: {message}"
                self.client_socket.send(formatted_message.encode('utf-8'))
            except:
                print("Ошибка отправки сообщения!")
                break

    def start_client(self):
        """Запуск клиента"""
        try:
            self.client_socket.connect((self.host, self.port))

            # Получение ника
            self.nickname = input("Введите ваш никнейм: ")

            # Запуск потока для получения сообщений
            receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
            receive_thread.start()

            print("Подключение успешно! Начинайте общение (для выхода введите 'exit')")
            print("-" * 50)

            # Основной поток для отправки сообщений
            self.send_messages()

        except Exception as e:
            print(f"Ошибка подключения: {e}")
        finally:
            self.client_socket.close()


if __name__ == "__main__":
    client = ChatClient()
    client.start_client()