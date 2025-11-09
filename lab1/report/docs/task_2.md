### Задание 2 (TCP, математика)
Сервер:
```bash
import socket


HOST = "localhost"
PORT = 10001


def recv_until_prompt(sock):
    data = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
        if data.endswith(b"> "):
            break
    return data


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(s.recv(4096).decode("utf-8", errors="replace"), end="")
        while True:

            data = recv_until_prompt(s)
            if not data:
                break
            print(data.decode("utf-8", errors="replace"), end="")
            line = input()
            s.sendall((line + "\n").encode("utf-8"))
            if line.lower() in ("exit", "quit"):
                print(s.recv(4096).decode("utf-8", errors="replace"), end="")
                break

            data = recv_until_prompt(s)
            print(data.decode("utf-8", errors="replace"), end="")


if __name__ == "__main__":
    main()

```

```bash
python task2_tcp_math/server_tcp_math.py
```


Клиент:
```bash
import socket
import threading
import math


HOST = "localhost"
PORT = 10001


HELP = (
    "Доступные операции:\n"
    "1) pythagoras a b            -> c = sqrt(a^2 + b^2)\n"
    "2) quadratic a b c           -> корни ax^2 + bx + c = 0\n"
    "3) trapezoid a b h           -> S = (a + b)/2 * h\n"
    "4) parallelogram base height -> S = base * height\n"
    "Например: quadratic 1 -3 2\n"
)


def handle(conn, addr):
    with conn:
        conn.sendall(HELP.encode('utf-8'))
        while True:
            conn.sendall(b"\n> ")
            data = b""
            while not data.endswith(b"\n"):
                chunk = conn.recv(4096)
                if not chunk:
                    return
                data += chunk
            line = data.decode("utf-8", errors="replace").strip()
            if not line:
                continue
            if line.lower() in ("exit", "quit"):
                conn.sendall(b"Bye!\n")
                return
            try:
                parts = line.split()
                op = parts[0].lower()
                if op == "pythagoras" and len(parts) == 3:
                    a, b = map(float, parts[1:3])
                    c = math.hypot(a, b)
                    conn.sendall(f"c = {c}\n".encode('utf-8'))
                elif op == "quadratic" and len(parts) == 4:
                    a, b, c = map(float, parts[1:4])
                    if a == 0:
                        conn.sendall("a=0 -> линейное уравнение, x = -c/b\n".encode('utf-8'))
                        continue
                    D = b*b - 4*a*c
                    if D > 0:
                        x1 = (-b + math.sqrt(D)) / (2*a)
                        x2 = (-b - math.sqrt(D)) / (2*a)
                        conn.sendall(f"Два корня: x1={x1}, x2={x2}\n".encode('utf-8'))
                    elif D == 0:
                        x = -b / (2*a)
                        conn.sendall(f"Один корень: x={x}\n".encode('utf-8'))
                    else:
                        real = -b / (2*a)
                        imag = math.sqrt(-D) / (2*a)
                        conn.sendall(f"Комплексные корни: {real}+{imag}i, {real}-{imag}i\n".encode('utf-8'))
                elif op == "trapezoid" and len(parts) == 4:
                    a, b, h = map(float, parts[1:4])
                    S = (a + b) / 2.0 * h
                    conn.sendall(f"S = {S}\n".encode('utf-8'))
                elif op == "parallelogram" and len(parts) == 3:
                    base, height = map(float, parts[1:3])
                    S = base * height
                    conn.sendall(f"S = {S}\n".encode('utf-8'))
                else:
                    conn.sendall("Неверный формат.\n".encode('utf-8'))
            except Exception as e:
                conn.sendall(f"Ошибка: {e}\n".format(e=e).encode('utf-8'))


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"[TCP MATH SERVER] Listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            print(f"[TCP MATH SERVER] Connection from {addr}")
            threading.Thread(target=handle, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    main()

```

```bash
python task2_tcp_math/client_tcp_math.py
```

#### Примеры команд на клиенте:
- pythagoras 3 4
- quadratic 1 -3 2
- trapezoid 3 5 2
- parallelogram 10 7
- exit