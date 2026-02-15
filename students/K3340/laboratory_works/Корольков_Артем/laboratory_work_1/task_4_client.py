import socket
import threading


class ChatClient:
    def __init__(self, host='localhost', port=12347):
        self.host = host
        self.port = port
        self.nickname = input("Введите ваш никнейм: ")
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def receive_messages(self):
        """Получает сообщения от сервера"""
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
        """Отправляет сообщения на сервер"""
        while True:
            message = input()
            if message.lower() == 'quit':
                self.client_socket.close()
                break
            formatted_message = f'{self.nickname}: {message}'
            self.client_socket.send(formatted_message.encode('utf-8'))

    def start(self):
        """Запускает клиент"""
        try:
            self.client_socket.connect((self.host, self.port))
            print("Подключение к чату установлено!")
            print("Введите сообщения. Для выхода введите 'quit'")

            # Поток для получения сообщений
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()

            # Основной поток для отправки сообщений
            self.send_messages()

        except Exception as e:
            print(f"Ошибка подключения: {e}")
        finally:
            self.client_socket.close()


if __name__ == "__main__":
    client = ChatClient()
    client.start()