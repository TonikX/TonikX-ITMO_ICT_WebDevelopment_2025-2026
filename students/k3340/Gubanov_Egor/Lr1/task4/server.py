import socket
import threading
from datetime import datetime

HOST = '127.0.0.1'
PORT = 8004
ENCODING = 'utf-8'

clients = {}
clients_lock = threading.Lock()

def broadcast(message, exclude_sock=None):
    """Отправляет сообщение всем клиентам кроме исключенного"""
    data = (message + "\n").encode(ENCODING)
    with clients_lock:
        for sock in list(clients.keys()):
            if sock is exclude_sock:
                continue
            try:
                sock.sendall(data)
            except Exception:
                remove_client(sock)

def remove_client(sock):
    """Удаляет клиента из чата"""
    with clients_lock:
        name = clients.pop(sock, None)
    try:
        sock.close()
    except:
        pass
    if name:
        broadcast(f"🔴 {name} покинул чат")

def handle_client(conn, addr):
    """Обрабатывает подключение клиента"""
    with conn:
        try:
            name = conn.recv(1024).decode(ENCODING).strip()
            if not name:
                name = f"Гость_{addr[1]}"

            with clients_lock:
                clients[conn] = name
            
            print(f"{name} присоединился к чату ({addr})")
            broadcast(f"{name} присоединился к чату")

            while True:
                try:
                    data = conn.recv(4096)
                    if not data:
                        break
                    msg = data.decode(ENCODING).strip()
                    if msg.lower() == '/quit':
                        break
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] {name}: {msg}")
                    broadcast(f"{name}: {msg}", exclude_sock=conn)
                except socket.error as e:
                    print(f"Соединение с {name} разорвано: {e}")
                    break
                
        except Exception as e:
            print(f"Ошибка клиента {addr}: {e}")
        finally:
            remove_client(conn)

def main():
    print("Многопользовательский чат сервер")
    print("=" * 40)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(10)
        
        print(f"Сервер запущен на {HOST}:{PORT}")
        print(f"Многопоточность: Включена")
        print(f"Максимум клиентов: 10")
        print("\nНажмите Ctrl+C для остановки...")
        
        try:
            while True:
                conn, addr = s.accept()
                thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
                thread.start()
        except KeyboardInterrupt:
            print("\n\nСервер останавливается...")
            with clients_lock:
                for sock in list(clients.keys()):
                    try:
                        sock.close()
                    except:
                        pass
            print("Все соединения закрыты")

if __name__ == '__main__':
    main()
