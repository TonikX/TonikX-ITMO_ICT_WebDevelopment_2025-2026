# chat_server.py
import socket
import threading

HOST = '127.0.0.1'
PORT = 9090
BUFFER_SIZE = 1024

CLIENTS = []

def broadcast(message, sender_socket):
    for client in CLIENTS:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                client.close()
                CLIENTS.remove(client)

def handle_client(client_socket, address):
    print(f"[ПОДКЛЮЧЕНО] {address}")
    
    # Запрос имени пользователя
    client_socket.send('NICKNAME'.encode('utf-8'))
    try:
        nickname = client_socket.recv(BUFFER_SIZE).decode('utf-8')
        
        # Сообщаем всем о новом участнике
        join_message = f"{nickname} присоединился к чату!".encode('utf-8')
        broadcast(join_message, client_socket)
        
        while True:
            try:
                message = client_socket.recv(BUFFER_SIZE)
                if not message:
                    break 
                
                full_message = f"<{nickname}>: ".encode('utf-8') + message
                print(f"[СООБЩЕНИЕ] {full_message.decode('utf-8')}")
                broadcast(full_message, client_socket)
                
            except:
                break

    finally:
        if client_socket in CLIENTS:
            CLIENTS.remove(client_socket)
            client_socket.close()
            leave_message = f"{nickname} покинул чат.".encode('utf-8')
            print(f"[ОТКЛЮЧЕНО] {address} ({nickname})")
            broadcast(leave_message, None) # Отправляем всем, включая себя


def run_server():
    # Создание и настройка TCP-сокета
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    
    print(f"TCP Чат-Сервер запущен на {HOST}:{PORT}")
    print("Ожидание подключений...")
    
    while True:
        client_socket, address = server.accept()
        CLIENTS.append(client_socket)
        
        # Запуск отдельного потока для обработки нового клиента
        thread = threading.Thread(target=handle_client, args=(client_socket, address))
        thread.start()
        
        print(f"[АКТИВНО] Текущее число пользователей: {threading.active_count() - 1}") 

if __name__ == '__main__':
    run_server()