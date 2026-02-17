import socket
import threading

HOST = "localhost"
PORT = 12345

clients = {}
lock = threading.Lock()

def broadcast(message, sender_conn=None):
    """Отправляет сообщение всем клиентам кроме отправителя"""
    with lock:
        clients_copy = clients.copy()
    
    disconnected = []
    for conn, nickname in clients_copy.items():
        if conn != sender_conn:
            try:
                conn.send(f"{message}\n".encode())
            except:
                disconnected.append(conn)
    
    if disconnected:
        with lock:
            for conn in disconnected:
                if conn in clients:
                    del clients[conn]

def handle_client(conn, addr):
    """Обрабатывает подключение одного клиента"""
    nickname = f"user_{addr[1]}"
    
    try:
        conn.send("Введите ваш никнейм: ".encode())
        nickname_data = conn.recv(1024).decode().strip()
        
        if nickname_data:
            nickname = nickname_data
        
        with lock:
            clients[conn] = nickname
        
        print(f"Клиент {nickname} подключился")
        broadcast(f"{nickname} присоединился к чату!")
        conn.send("Вы в чате! Команды: /list, /quit\n".encode())
        
        while True:
            message = conn.recv(1024).decode().strip()
            
            if not message:
                break
                
            print(f"Получено от {nickname}: {message}")
            
            if message == "/quit":
                conn.send("До свидания!\n".encode())
                print(f"Клиент {nickname} вышел по команде")
                break
            elif message == "/list":
                with lock:
                    users = ", ".join(clients.values())
                conn.send(f"Участники чата: {users}\n".encode())
            else:
                broadcast(f"{nickname}: {message}", conn)
                
    except Exception as e:
        print(f"Ошибка с клиентом {nickname}: {e}")
    finally:
        with lock:
            if conn in clients:
                del clients[conn]
                print(f"Клиент {nickname} удален из списка")
        
        broadcast(f"{nickname} покинул чат")
        
        try:
            conn.close()
        except:
            pass

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        
        print(f"Чат-сервер запущен на {HOST}:{PORT}")
        
        try:
            while True:
                conn, addr = server.accept()
                print(f"Новое подключение от {addr}")
                thread = threading.Thread(target=handle_client, args=(conn, addr))
                thread.daemon = True
                thread.start()
        except KeyboardInterrupt:
            print("\nСервер остановлен")
        except Exception as e:
            print(f"Ошибка сервера: {e}")

if __name__ == "__main__":
    main()