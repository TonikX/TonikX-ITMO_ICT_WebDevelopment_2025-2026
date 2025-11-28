import socket
import threading

clients = []  

def handle_client(client_socket, addr):
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if not msg:
                break
            print(f'[{addr}] {msg}')
            for c in clients:
                if c != client_socket:
                    c.send(f'[{addr}] {msg}'.encode())
        except:
            break
    client_socket.close()
    clients.remove(client_socket)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8888))
server_socket.listen()
print('Сервер чата запущен…')


while True:
    client_socket, addr = server_socket.accept()
    clients.append(client_socket)
    print(f'Новый клиент: {addr}')
    thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    thread.start()
