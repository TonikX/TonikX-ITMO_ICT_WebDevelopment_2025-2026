import socket

HOST = 'localhost'
PORT = 8080

def tcp_client():
    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((HOST, PORT))
        
        print("\n=== Вычисление площади параллелограмма ===")
        print("Формула: S = a * h")
        
        base = input("Введите основание параллелограмма: ")
        height = input("Введите высоту параллелограмма: ")
        
        message = f"{base} {height}"
        conn.send(message.encode('utf-8'))
        
        response = conn.recv(1024).decode('utf-8')
        print(f"\nОтвет от сервера: {response}")
        
    except ConnectionRefusedError:
        print("Ошибка: Не удалось подключиться к серверу")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        conn.close()
        print("Соединение закрыто")

if __name__ == "__main__":
    tcp_client()