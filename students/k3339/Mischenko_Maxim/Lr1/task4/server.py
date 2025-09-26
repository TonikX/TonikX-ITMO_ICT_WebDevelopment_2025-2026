import threading
import socket


class Server:
    def __init__(self):
        self.clients = {}
        self.server_socket = None
        self.host = '127.0.0.1'
        self.port = 8080

    def listen(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            print(f'server socket bound to {self.host}:{self.port}')

            self.server_socket.listen(64)
            while True:
                client_socket, client_address = self.server_socket.accept()
                thread = threading.Thread(target=self.client_connect, args=(client_socket, client_address))
                thread.start()
        finally:
            self.server_socket.close()


    def client_connect(self, client_socket, client_address):
        print(f'Got connection from {client_address}')
        client_name = client_socket.recv(1024).decode()
        if client_name not in self.clients:
            self.clients[client_name] = (client_socket, client_address)
            client_socket.sendall(f'Welcome, {client_name}!'.encode())
            print(f'New User: {client_name}')

        while True:
            try:
                message = client_socket.recv(1024).decode()
                print(f'New message from {client_name}: {message}')
                if not message:
                    break
                for name, (socket, address) in self.clients.items():
                    if socket != client_socket:
                        socket.sendall(f'{client_name}: {message}'.encode())
            except:
                break
        del self.clients[client_name]
        client_socket.close()
        print(f'{client_name} has disconnected')

if __name__ == '__main__':
    server = Server()
    server.listen()
