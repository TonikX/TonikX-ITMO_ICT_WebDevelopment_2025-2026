import socket
import math

HOST = 'localhost'
PORT = 8080

def parse_floats(parts, n):
    try:
        vals = [float(x) for x in parts[1:1+n]]
        if len(vals) != n:
            return None, "Ошибка: неправильное число аргументов."
        return vals, None
    except ValueError:
        return None, "Ошибка: параметры должны быть числами."

def handle_request(req: str) -> str:
    parts = req.strip().split()
    if not parts:
        return "Ошибка: пустой запрос."
    op = parts[0].upper()

    if op == 'PYTH':
        vals, err = parse_floats(parts, 2)
        if err: return err
        a, b = vals
        if a <= 0 or b <= 0:
            return "Ошибка: a и b должны быть > 0."
        c = math.hypot(a, b)
        return f"Гипотенуза: {c:.6g}"

    elif op == 'QUAD':
        vals, err = parse_floats(parts, 3)
        if err: return err
        a, b, c = vals
        if a == 0.0:
            if b == 0.0:
                return "Нет решений (a=0 и b=0)."
            x = -c / b
            return f"Линейное уравнение, x = {x:.6g}"
        D = b*b - 4*a*c
        if D > 0:
            sqrtD = math.sqrt(D)
            x1 = (-b + sqrtD) / (2*a)
            x2 = (-b - sqrtD) / (2*a)
            return f"Два корня: x1 = {x1:.6g}, x2 = {x2:.6g}"
        elif D == 0:
            x = -b / (2*a)
            return f"Один корень: x = {x:.6g}"
        else:
            return "Нет вещественных корней."

    elif op == 'TRAP':
        vals, err = parse_floats(parts, 3)
        if err: return err
        a, b, h = vals
        if a <= 0 or b <= 0 or h <= 0:
            return "Ошибка: a, b, h должны быть > 0."
        area = (a + b) / 2 * h
        return f"Площадь трапеции: {area:.6g}"

    elif op == 'PARA':
        vals, err = parse_floats(parts, 2)
        if err: return err
        a, h = vals
        if a <= 0 or h <= 0:
            return "Ошибка: a и h должны быть > 0."
        area = a * h
        return f"Площадь параллелограмма: {area:.6g}"

    else:
        return "Ошибка: неизвестная операция."

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"TCP сервер запущен на {HOST}:{PORT}...")

while True:
    conn, addr = server_socket.accept()
    print("Клиент подключился:", addr)
    data = conn.recv(1024)
    if not data:
        conn.close()
        continue
    req = data.decode('utf-8', errors='ignore')
    print("Запрос:", req.strip())
    resp = handle_request(req)
    conn.sendall((resp + "\n").encode('utf-8'))
    conn.close()
