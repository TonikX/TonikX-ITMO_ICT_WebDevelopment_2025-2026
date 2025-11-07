import socket
import threading
import time

HOST = "localhost"
PORT = 12345

def receive_messages(sock):
    """Получает сообщения от сервера"""
    while True:
        try:
            message = sock.recv(1024).decode()
            if not message:
                print("\nСервер закрыл соединение")
                break
            print(message, end="")
        except:
            break

def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((HOST, PORT))
            
            receiver = threading.Thread(target=receive_messages, args=(client,))
            receiver.daemon = True
            receiver.start()
            
            print("Подключение к чату установлено!")
            
            try:
                while True:
                    message = input()
                    
                    if message.strip() == "/quit":
                        client.send(b"/quit\n")
                        time.sleep(0.1)
                        break
                    else:
                        client.send(f"{message}\n".encode())
                        
            except KeyboardInterrupt:
                print("\nВыход из чата...")
                client.send(b"/quit\n")
                time.sleep(0.1)
            
    except ConnectionRefusedError:
        print("Не удалось подключиться к серверу")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()