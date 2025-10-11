from math import sqrt
import socket

HOST = 'localhost'
PORT = 12345
BUFFER_SIZE = 1024

def solve_equation(a, b, c):
    if a == 0:
        if b == 0:
            if c == 0:
                return "Уравнение имеет бесконечное количество решений"
            else:
                return "Уравнение не имеет решений"
        else:
            x = -c / b
            return f"Это линейное уравнение. Корень: x = {x:.2f}"
    
    D = b**2 - 4 * a * c

    if D < 0:
        return "У уравнения нет действительных корней"
    elif D == 0:
        x = -b / (2 * a)
        return f"Уравнение имеет один корень: x = {x:.2f}"
    else:
        x_1 = (-b - sqrt(D)) / (2 * a)
        x_2 = (-b + sqrt(D)) / (2 * a)
        return f"Уравнение имеет два корня: x₁ = {x_1:.2f}, x₂ = {x_2:.2f}"
    
    

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"TCP сервер запущен на {HOST}:{PORT}")

        while True:
            try:
                conn, client_addr = s.accept()
                print(f"Соединение от {client_addr}")
                
                with conn:
                    data = conn.recv(BUFFER_SIZE)
                    if not data:
                        continue
                    
                    try:
                        values = data.decode("utf-8").split()
                        if len(values) != 3:
                            error_msg = "Ошибка: требуется 3 коэффициента (a b c)"
                            conn.sendall(error_msg.encode("utf-8"))
                            continue
                            
                        a, b, c = map(float, values)
                        result = solve_equation(a, b, c)
                        conn.sendall(result.encode("utf-8"))
                        
                    except ValueError:
                        error_msg = "Ошибка: все коэффициенты должны быть числами"
                        conn.sendall(error_msg.encode("utf-8"))
                    except Exception as e:
                        error_msg = f"Ошибка обработки: {str(e)}"
                        conn.sendall(error_msg.encode("utf-8"))
                        
            except KeyboardInterrupt:
                print("Сервер остановлен")
                break
            except Exception as e:
                print(f"Ошибка сервера: {e}")
                continue

if __name__ == "__main__":
    main()