import socket
import threading

HOST = "127.0.0.1"
PORT = 30114

clients = []

def handle_client(conn, addr):
    print(f"Connected {addr}")
    while True:
        try:
            msg = conn.recv(1996).decode()
            if not msg:
                break
            # формируем сообщение с указанием порта клиента
            full_msg = f"Message from [{addr[1]}]: {msg}"
            print(full_msg)  # отображаем на сервере
            broadcast(full_msg, conn)
        except:
            break
    conn.close()
    clients.remove(conn)
    print(f"{addr} disconnected")

def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            client.sendall(message.encode())

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
print(f"Chat-server is running on {HOST}:{PORT}")

while True:
    conn, addr = server_socket.accept()
    clients.append(conn)
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
