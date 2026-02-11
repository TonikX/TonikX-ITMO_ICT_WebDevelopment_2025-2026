import socket
import threading

clients = []

def broadcast(message, _socket):
    for client in clients:
        if client != _socket:
            try:
                client.send(message)
            except:
                clients.remove(client)

def handle(conn):
    while True:
        try:
            message = conn.recv(1024)
            broadcast(message, conn)
        except:
            clients.remove(conn)
            conn.close()
            break

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 5555))
server.listen()

while True:
    conn, addr = server.accept()
    clients.append(conn)
    threading.Thread(target=handle, args=(conn,)).start()