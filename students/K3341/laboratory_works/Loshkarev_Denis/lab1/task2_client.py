# tcp_client_task2_quad_min.py - Сокращенный вариант
import socket

HOST = '127.0.0.1'
PORT = 8889

def run_client_quad_min():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            
            user_input = input("Введите коэффициенты (напр.: a=1,b=-5,c=6): ")
            s.sendall(user_input.encode('utf-8'))
            print(f"Отправлено: {user_input}")
            
            data = s.recv(1024)
            if data:
                print(f"✅ Результат: {data.decode('utf-8')}")

        except ConnectionRefusedError:
            print("❌ Ошибка: Сервер недоступен.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

if __name__ == '__main__':
    run_client_quad_min()