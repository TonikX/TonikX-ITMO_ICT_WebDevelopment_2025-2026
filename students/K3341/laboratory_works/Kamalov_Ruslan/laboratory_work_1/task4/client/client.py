import socket
import threading
from cfg import SERVER_HOST, SERVER_PORT, BUFFER_SIZE

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            if message:
                print(f"\r{message}\n[Вы]: ", end='')
            else:
                break
        except:
            print("\n[!] Соединение с сервером потеряно")
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print("=" * 45)
        print("Многопользовательский чат")
        print("=" * 45)
        
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print(f"[+] Подключено к серверу {SERVER_HOST}:{SERVER_PORT}")
        
        username = input("[?] Введите ваше имя: ").strip()
        client_socket.send(username.encode('utf-8'))
        print("-" * 45)
        print("[*] Вы в чате! Для выхода введите 'exit'")
        print("-" * 45)
        
        receive_thread = threading.Thread(
            target=receive_messages,
            args=(client_socket,)
        )
        receive_thread.daemon = True
        receive_thread.start()
        
        while True:
            message = input("[Вы]: ")
            
            if message.lower() == 'exit':
                print("[*] Выход из чата...")
                break
            
            if message:
                client_socket.send(message.encode('utf-8'))
    except Exception as e:
        print(f"[!] Ошибка: {e}")
    finally:
        client_socket.close()
        print("[*] Отключено от сервера")

if __name__ == "__main__":
    start_client()
