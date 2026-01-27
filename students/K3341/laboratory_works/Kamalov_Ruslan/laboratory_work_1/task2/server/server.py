import socket
from cfg import SERVER_HOST, SERVER_PORT, BUFFER_SIZE

def calc(a, b):
    return (a**2 + b**2) ** 0.5

def start_tcp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(1)

    print(f"[*] TCP Сервер запущен на {SERVER_HOST}:{SERVER_PORT}")
    print("[*] Ожидание подключения клиента...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"\n[+] Подключен клиент: {client_address}")
            
            data = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            if data:
                print(f"[+] Получены данные: {data}")  

                a, b = map(float, data.split(','))
                print(f"[+] Катет a = {a}, катет b = {b}")

                result = calc(a, b)
                print(f"[+] Вычислена гипотенуза: c = {result:.4f}")

                client_socket.send(str(result).encode('utf-8'))
                print(f"[+] Результат отправлен клиенту")
                
            client_socket.close()
            print(f"[*] Соединение с {client_address} закрыто")
            
    except KeyboardInterrupt:
        print("\n[!] Сервер остановлен пользователем")
    finally:
        server_socket.close()
        print("[*] Сокет закрыт")

if __name__ == "__main__":
    start_tcp_server()
