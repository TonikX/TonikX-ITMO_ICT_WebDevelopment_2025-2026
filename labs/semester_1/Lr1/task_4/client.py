import socket
import threading


class ChatClient:
    """
    Консольный клиент для реализации интерфейса чата в консоли пользователя.
    """
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True
    
    def receive_messages(self):
        """
        Получение сообщений от сервера.
        """
        while self.running:
            try:
                # Получаем сообщение от сервера и выводим его пользователю
                message = self.client_socket.recv(4096).decode('utf-8')
                if message:
                    # Задаём дополнительные параметры print для удобства отображения интерфейса чата
                    print(f"\r{message}\n[Вы] ", end="", flush=True)
            except:
                # При ошибке считаем соединение разорваны и завершаем работу клиента
                print("\r[СЕРВЕР] Соединение разорвано")
                self.running = False
                break
    
    def send_message(self, message):
        """
        Отправка сообщения на сервер.
        """
        try:
            self.client_socket.send(message.encode('utf-8'))
        except:
            print("[ОШИБКА] Не удалось отправить сообщение")
    
    def start(self):
        """
        Запуск консольного клиента.
        """
        print("Многопользовательский чат")
        username = input("Введите ваше имя: ")
        
        try:
            self.client_socket.connect((self.host, self.port))

            # Первым сообщением отправляем имя пользователя
            self.send_message(username)

            # Запускаем приём сообщений от сервера в отдельном потоке
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()

            print("\nДобро пожаловать в чат! Для выхода введите '/exit'")
            print("[Вы] ", end="")

            # Цикл для отправки сообщений пользователя
            while self.running:
                try:
                    message = input()
                    if message.strip() == '/exit':
                        self.running = False
                        break
                    if message.strip():
                        self.send_message(message)
                    print("[Вы] ", end="")

                except Exception as e:
                    print(f"[ОШИБКА] {e}")
                    break
        
        except Exception as e:
            print(f"[ОШИБКА] {e}")
        finally:
            self.running = False
            self.client_socket.close()
            print("\nДо свидания!")


if __name__ == "__main__":
    client = ChatClient()
    client.start()
