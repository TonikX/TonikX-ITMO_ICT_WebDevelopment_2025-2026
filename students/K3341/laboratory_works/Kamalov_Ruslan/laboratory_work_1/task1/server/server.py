import socket
from cfg import SERVER_HOST, SERVER_PORT, BUFFER_SIZE

def start_udp_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    
    server_socket.bind((SERVER_HOST, SERVER_PORT))

    print(f"[*] UDP Сервер запущен на {SERVER_HOST}:{SERVER_PORT}")
    print("[*] Ожидание сообщений от клиента...")

    try:
        while True:
            data, client_address = server_socket.recvfrom(BUFFER_SIZE)
            message = data.decode('utf-8')
            print(f"\n[+] Получено сообщение от {client_address}")
            print(f"[+] Содержимое: {message}")
            
            response = "Hello, client"
            server_socket.sendto(response.encode('utf-8'), client_address)
            print(f"[+] Ответ отправлен клиенту: {response}")
            
    except KeyboardInterrupt:
        print("\n[!] Сервер остановлен пользователем")
    finally:
        server_socket.close()
        print("[*] Сокет закрыт")

if __name__ == "__main__":
    start_udp_server()
