import socket
import threading


class ChatClient:
    def __init__(self, host='localhost', port=8911):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = False

    def start(self):
        try:
            self.socket.connect((self.host, self.port))
            self.running = True
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()

            print("Подключение к чату установлено. Для выхода введите /quit")
            while self.running:
                message = input()
                if message == '/quit':
                    break
                self.socket.send(message.encode())
        except Exception as e:
            print(f"Ошибка подключения: {e}")
        finally:
            self.stop()

    def receive_messages(self):
        while self.running:
            try:
                message = self.socket.recv(1024).decode()
                if not message:
                    break
                print(message)
            except:
                break

    def stop(self):
        self.running = False
        self.socket.close()
        print("Отключение от чата")


if __name__ == "__main__":
    client = ChatClient()
    client.start()