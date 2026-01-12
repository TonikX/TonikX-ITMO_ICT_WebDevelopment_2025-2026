import socket
import threading

HOST = 'localhost'
PORT = 8080

clients = {}
chat_history = []
clients_lock = threading.Lock()

def remove_client_silent(client_socket):
    with clients_lock:
        if client_socket in clients:
            client_name = clients[client_socket]
            del clients[client_socket]
            print(f"Клиент {client_name} отключен")
    
    try:
        client_socket.close()
    except:
        pass

def broadcast_message(message: str, sender_name: str = '', exclude_client: bool = None):
    if sender_name:
        formatted_message = f"[{sender_name}]: {message}"
    else:
        formatted_message = message
    
    chat_history.append(formatted_message)
    
    with clients_lock:
        disconnected_clients = []
        for client_socket in list(clients.keys()):
            if client_socket != exclude_client:
                try:
                    client_socket.send(formatted_message.encode('utf-8'))
                except:
                    disconnected_clients.append(client_socket)
        
        for client in disconnected_clients:
            remove_client_silent(client)

def remove_client(client_socket):
    with clients_lock:
        if client_socket in clients:
            client_name = clients[client_socket]
            del clients[client_socket]
            print(f"Клиент {client_name} отключен")
            
            broadcast_message(f"{client_name} покинул чат", exclude_client=client_socket)
    
    try:
        client_socket.close()
    except:
        pass

def handle_client(client_socket):
    client_name = None
    
    try:
        client_socket.send("Введите ваше имя: ".encode('utf-8'))
        client_name = client_socket.recv(1024).decode('utf-8').strip()
        
        if not client_name:
            client_name = "Anonymous"
        
        with clients_lock:
            clients[client_socket] = client_name
        
        print(f"Клиент {client_name} подключился")
        
        broadcast_message(f"{client_name} присоединился к чату")
        
        if chat_history:
            history_text = "\n--- История чата ---\n" + "\n".join(chat_history[-10:]) + "\n--- Конец истории ---\n"
            try:
                client_socket.send(history_text.encode('utf-8'))
            except:
                pass

        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8').strip()
                
                if not message:
                    break
                    
                if message.lower() == 'exit':
                    break
                
                broadcast_message(message, client_name)
                
            except ConnectionResetError:
                print(f"Клиент {client_name} неожиданно отключился")
                break
            except Exception as e:
                print(f"Ошибка получения сообщения от {client_name}: {e}")
                break
            
    except Exception as e:
        print(f"Ошибка при обработке клиента {client_name}: {e}")
    finally:
        remove_client(client_socket)

def accept_connections(server_socket):
    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Подключение от {client_address}")
            
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.daemon = True
            client_thread.start()
            
        except Exception as e:
            print(f"Ошибка при принятии подключения: {e}")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Сервер запущен на {HOST}:{PORT}")
        print("Ожидание подключений...")
        
        accept_connections(server_socket)
        
    except KeyboardInterrupt:
        print("\nСервер остановлен")
    except Exception as e:
        print(f"Ошибка сервера: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()