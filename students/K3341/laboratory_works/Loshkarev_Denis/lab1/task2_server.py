import socket
import math
import cmath

HOST = '127.0.0.1'
PORT = 8889

def solve_quadratic_min(data_str):
    """Парсит данные и решает ax^2 + bx + c = 0."""
    params = {}
    try:
        for part in data_str.split(','):
            key, val = part.strip().split('=')
            params[key.lower()] = float(val)
        a, b, c = params.get('a'), params.get('b'), params.get('c')
    except:
        return "Ошибка: Проверьте формат ввода (a=X, b=Y, c=Z) и значения."
        
    if a is None or b is None or c is None:
        return "Ошибка: Не все коэффициенты (a, b, c) предоставлены."
    
    if a == 0:
        return f"a=0. Корень x = {-c/b:.3f}" if b != 0 else "Уравнение вырождается."

    D = b**2 - 4 * a * c
    
    if D > 0:
        x1 = (-b + math.sqrt(D)) / (2 * a)
        x2 = (-b - math.sqrt(D)) / (2 * a)
        return f"D > 0. x1 = {x1:.3f}, x2 = {x2:.3f}"
    
    elif D == 0:
        x = -b / (2 * a)
        return f"D = 0. Корень x = {x:.3f}"
        
    else: 
        x1 = (-b + cmath.sqrt(D)) / (2 * a)
        x2 = (-b - cmath.sqrt(D)) / (2 * a)
        return f"D < 0. x1 = {x1}, x2 = {x2}"


def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"Сервер (Квадратное уравнение) запущен на {HOST}:{PORT}. Ожидание...")
        
        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(1024).decode('utf-8')
                if not data: continue
                
                result = solve_quadratic_min(data)
                conn.sendall(result.encode('utf-8'))
                print(f"Обработан запрос от {addr}. Ответ: {result}")

if __name__ == '__main__':
    run_server()