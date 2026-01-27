import socket
from cfg import SERVER_HOST, SERVER_PORT, BUFFER_SIZE

def start_tcp_client():
    print("=" * 45)
    print("Теорема Пифагора: a² + b² = c²")
    print("=" * 45)
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(5.0)
    
    try:
        a = float(input("[?] Введите катет a: "))
        b = float(input("[?] Введите катет b: "))
        
        print(f"\n[*] Подключение к серверу {SERVER_HOST}:{SERVER_PORT}")
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("[+] Подключение установлено")
        
        message = f"{a},{b}"
        client_socket.send(message.encode('utf-8'))
        print(f"[+] Данные отправлены: a={a}, b={b}")
        print("[*] Ожидание ответа...")
        
        data = client_socket.recv(BUFFER_SIZE).decode('utf-8')
        result = float(data)
        
        print(f"\n[+] Получен ответ от сервера")
        print("-" * 45)
        print(f"Гипотенуза c = {result:.4f}")
        print("=" * 45)
        
    except socket.timeout:
        print("[!] Ошибка: превышено время ожидания ответа")
    except Exception as e:
        print(f"[!] Ошибка: {e}")
    finally:
        client_socket.close()
        print("[*] Сокет закрыт")

if __name__ == "__main__":
    start_tcp_client()
