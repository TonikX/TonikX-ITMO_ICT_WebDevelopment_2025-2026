import socket
import threading
import sys

HOST = '127.0.0.1'
PORT = 9090
BUFFER_SIZE = 1024

def receive_messages(client_socket):
    while True:
        try:
            # Получение данных
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                print("\n[!] Соединение с сервером потеряно.")
                client_socket.close()
                sys.exit()
            
            message = data.decode('utf-8')
            
            if message == 'NICKNAME':
                pass 
            else:
                print(message)
                
        except Exception as e:
            print("\n[!] Произошла ошибка при получении данных.")
            client_socket.close()
            break

def run_client():
    nickname = input("Введите ваш никнейм: ")
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
    except ConnectionRefusedError:
        print(f"❌ Ошибка: Не удалось подключиться к серверу на {HOST}:{PORT}.")
        return

    client.send(nickname.encode('utf-8'))
    
    print("--- Успешно подключено. Можете начать чат (введите 'quit' для выхода) ---")

    # Запуск потока для приема сообщений
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.daemon = True # Позволяет потоку завершиться при завершении основной программы
    receive_thread.start()

    while True:
        try:
            message = input()
            if message.lower() == 'quit':
                print("Выход из чата...")
                break
                
            client.send(message.encode('utf-8'))
        except Exception:
            break

    client.close()

if __name__ == '__main__':
    run_client()