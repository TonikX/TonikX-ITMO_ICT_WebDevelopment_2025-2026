import socket
from cfg import SERVER_HOST, SERVER_PORT, BUFFER_SIZE

def start_udp_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(5.0)
    try:
        message = "Hello, server"
        print(f"[*] Отправка сообщения серверу {SERVER_HOST}:{SERVER_PORT}")
        print(f"[*] Сообщение: {message}")
        client_socket.sendto(message.encode('utf-8'), (SERVER_HOST, SERVER_PORT))
        print("[*] Сообщение отправлено, ожидание ответа...")
        
        data, server_address = client_socket.recvfrom(BUFFER_SIZE)
        response = data.decode('utf-8')
        print(f"\n[+] Получен ответ от сервера {server_address}")
        print(f"[+] Содержимое: {response}")
    except socket.timeout:
        print("[!] Ошибка: превышено время ожидания ответа от сервера")
    except Exception as e:
        print(f"[!] Ошибка: {e}")
    finally:
        client_socket.close()
        print("[*] Сокет закрыт")

if __name__ == "__main__":
    start_udp_client()
