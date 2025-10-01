import threading
import socket


class Client:
    def __init__(self, name):
        self.name = name
        self.host = 'localhost'
        self.port = 8080
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if not message:
                    break
                print(message)
            except:
                break

    def connect_to_chat(self):
        self.client_socket.connect((self.host, self.port))
        print(f'Connected to {self.host}:{self.port}')

        self.client_socket.sendall(self.name.encode())

        thread = threading.Thread(target=self.receive_messages, daemon=True)
        thread.start()

        while True:
            message = input()
            if message.lower() == '/exit':
                break
            self.client_socket.sendall(message.encode())
        
        self.client_socket.close()


if __name__ == '__main__':
    client = Client(input('Enter your name: '))
    client.connect_to_chat()
