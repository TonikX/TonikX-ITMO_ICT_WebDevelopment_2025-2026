import socket

HOST = 'localhost'
PORT = 12345
BUFFER_SIZE = 1024

def get_equation_coef(coef):
    while True:
        try:
            value = input(coef).strip().replace(",", ".")
            return float(value)
        except ValueError:
            print("Ошибка: введите число!")

def main():
    print("Решение квадратного уравнения: ax² + bx + c = 0\n")

    a = get_equation_coef("Введите коэффициент a: ")
    b = get_equation_coef("Введите коэффициент b: ")
    c = get_equation_coef("Введите коэффициент c: ")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.settimeout(10.0)
            s.connect((HOST, PORT))
            
            message = f"{a} {b} {c}"
            s.sendall(message.encode("utf-8"))
            
            data = s.recv(BUFFER_SIZE)
            response = data.decode("utf-8")
            print(f"\nРезультат: {response}")
            
        except ConnectionRefusedError:
            print("Ошибка: не удалось подключиться к серверу")
        except socket.timeout:
            print("Ошибка: превышено время ожидания ответа от сервера")
        except ConnectionResetError:
            print("Ошибка: соединение было разорвано сервером")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()