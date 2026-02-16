import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("localhost", 9999))
server.listen()
print("Server is running...")
clients = {}

def broadcast(message, sender=None):
    for client in clients:
        if client != sender:
            try:
                client.send(message.encode())
            except:
                remove(client)

def remove(conn):
    if conn in clients:
        name = clients.pop(conn)
        conn.close()
        broadcast(f"{name} left the chat")

def handle(conn, addr):
    try:
        name = conn.recv(1024).decode()
        clients[conn] = name
        print(f"{name} connected from {addr}")
        broadcast(f"{name} joined the chat")
        while True:
            msg = conn.recv(1024).decode()
            if not msg:
                break
            print(f"{name}: {msg}")
            broadcast(f"{name}: {msg}", conn)
    except:
        pass
    finally:
        remove(conn)

while True:
    conn, addr = server.accept()
    threading.Thread(target=handle, args=(conn, addr), daemon=True).start()
