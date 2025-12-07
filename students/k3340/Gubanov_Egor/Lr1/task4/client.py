import socket
import threading
import sys
import time

HOST = '127.0.0.1'
PORT = 8004
ENCODING = 'utf-8'

def recv_messages(sock, stop_event):
    """Получает сообщения от сервера"""
    try:
        while not stop_event.is_set():
            try:
                data = sock.recv(4096)
                if not data:
                    print("\nСоединение закрыто сервером")
                    break
                sys.stdout.write(data.decode(ENCODING))
                sys.stdout.flush()
            except socket.error as e:
                if stop_event.is_set():
                    break
                print(f"\nОшибка получения: {e}")
                break
    except Exception as e:
        if not stop_event.is_set():
            print(f"\nОшибка получения: {e}")

def main():
    print("Многопользовательский чат")
    print("=" * 30)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Подключен к серверу {HOST}:{PORT}")

        stop_event = threading.Event()
        recv_thread = threading.Thread(target=recv_messages, args=(s, stop_event), daemon=True)
        recv_thread.start()

        name = input("Введите ваше имя: ").strip()
        if not name:
            name = "Анонимный"
        s.sendall((name + "\n").encode(ENCODING))

        print(f"Добро пожаловать, {name}! Введите сообщения (или /quit для выхода)")
        print("-" * 50)
        
        try:
            while True:
                msg = input()
                if msg.strip().lower() == "/quit":
                    s.sendall(msg.encode(ENCODING))
                    break
                s.sendall(msg.encode(ENCODING))
        except KeyboardInterrupt:
            print("\nПрерывание...")
        finally:
            stop_event.set()
            print("👋 Отключение от чата...")
            time.sleep(0.1)

if __name__ == '__main__':
    main()
