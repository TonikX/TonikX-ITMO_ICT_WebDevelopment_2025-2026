import socket
import threading

HOST = 'localhost'
PORT = 8080

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                break
        except:
            break

def send_messages(client_socket):
    while True:
        try:
            message = input()
            if message.lower() == 'exit':
                break
            client_socket.send(message.encode('utf-8'))
        except:
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((HOST, PORT))

        name_request = client_socket.recv(1024).decode('utf-8')
        print(name_request, end='')

        name = input()
        if not name:
            name = "Anonymous"
        client_socket.send(name.encode('utf-8'))

        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.daemon = True
        receive_thread.start()
        
        send_messages(client_socket)
        
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()