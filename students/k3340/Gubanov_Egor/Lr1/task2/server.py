import socket
import json
import math

HOST = '127.0.0.1'
PORT = 8002
ENCODING = 'utf-8'

def solve_quadratic(a, b, c):
    if a == 0:
        raise ValueError("a не должно быть 0")
    
    disc = b*b - 4*a*c
    if disc < 0:
        return "Нет действительных корней"
    elif disc == 0:
        x = -b / (2*a)
        return f"Один корень: x = {x:.2f}"
    else:
        sqrt_d = math.sqrt(disc)
        x1 = (-b + sqrt_d) / (2*a)
        x2 = (-b - sqrt_d) / (2*a)
        return f"Два корня: x1 = {x1:.2f}, x2 = {x2:.2f}"

def handle_request(data):
    try:
        req = json.loads(data)
        params = req.get("params", [])
        if len(params) != 3:
            raise ValueError("Нужны 3 параметра: a, b, c")
        
        a, b, c = map(float, params)
        result = solve_quadratic(a, b, c)
        return json.dumps({"status": "ok", "result": result}) + "\n"
    except Exception as e:
        return json.dumps({"status": "error", "error": str(e)}) + "\n"

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"TCP сервер квадратных уравнений на {HOST}:{PORT}")
        try:
            while True:
                conn, addr = s.accept()
                with conn:
                    print(f"Подключен: {addr}")

                    request = ""
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        request += data.decode(ENCODING)
                        if "\n" in request:
                            break
                    
                    response = handle_request(request.strip())
                    conn.sendall(response.encode(ENCODING))
        except KeyboardInterrupt:
            print("\nСервер завершает работу.")

if __name__ == '__main__':
    main()
