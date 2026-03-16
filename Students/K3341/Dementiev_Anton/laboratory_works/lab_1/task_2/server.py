import socket
import threading
import math

HOST = "127.0.0.1"
PORT = 12345


def solve_quadratic(a: float, b: float, c: float) -> str:
    D = b**2 - 4 * a * c
    if D < 0:
        return "Нет действительных корней"
    elif D == 0:
        x = -b / (2 * a)
        return f"Один корень: {x}"
    else:
        x1 = (-b + math.sqrt(D)) / (2 * a)
        x2 = (-b - math.sqrt(D)) / (2 * a)
        return f"Два корня: {x1}, {x2}"


def handle_client(conn, addr):
    print(f"[+] Подключен клиент {addr}")
    try:
        data = conn.recv(1024).decode()
        if not data:
            return
        print(f"[{addr}] {data}")
        a, b, c = map(float, data.split())
        result = solve_quadratic(a, b, c)
        conn.sendall(result.encode())
    except Exception as e:
        print(f"Ошибка с клиентом {addr}: {e}")
    finally:
        conn.close()
        print(f"[-] Клиент {addr} отключился")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Сервер слушает на {HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()
