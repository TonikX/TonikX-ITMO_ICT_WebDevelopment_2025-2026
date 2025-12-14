import socket
import threading

clients = []
lock = threading.Lock()

def handle_client(client_socket, addr):
    print(f"Подключен клиент: {addr}")
    with lock:
        clients.append(client_socket)
    
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            
            message = data.decode('utf-8')
            print(f"Сообщение от {addr}: {message}")
            
            with lock:
                for client in clients:
                    if client != client_socket:
                        try:
                            client.send(f"{addr}: {message}".encode('utf-8'))
                        except:
                            pass
        except:
            break
    
    with lock:
        clients.remove(client_socket)
    client_socket.close()
    print(f"Клиент {addr} отключен")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8891))
server_socket.listen(10)

print("Чат сервер запущен на порту 8891")

while True:
    client_socket, addr = server_socket.accept()
    thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    thread.start()

