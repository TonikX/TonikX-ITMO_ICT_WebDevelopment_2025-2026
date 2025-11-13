import socket, json

HOST = "127.0.0.1"
PORT = 9998

MENU = '''
1) Теорема Пифагора
2) Квадратное уравнение
3) Площадь трапеции
4) Площадь параллелограмма
Выберите операцию: 
'''

def main():
    op = input(MENU).strip().lower()
    params = {}
    if op in ("1","pythagoras"):
        params["a"] = input("a = ")
        params["b"] = input("b = ")
    elif op in ("2","quadratic"):
        params["a"] = input("a = ")
        params["b"] = input("b = ")
        params["c"] = input("c = ")
    elif op in ("3","trapezoid_area"):
        params["a"] = input("a = ")
        params["b"] = input("b = ")
        params["h"] = input("h = ")
    elif op in ("4","parallelogram_area"):
        params["a"] = input("a = ")
        params["h"] = input("h = ")
    else:
        print("Неизвестная операция")
        return

    req = {"operation": op, "params": params}
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(json.dumps(req).encode("utf-8"))
        data = s.recv(4096)
        print("Ответ:", data.decode("utf-8"))

if __name__ == "__main__":
    main()
