import socket
import math
from students.k3339.Shafikov_Maxim.Lr1.config import host, port


if __name__ == "__main__":
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind((host, port))
    tcp_socket.listen(5)
    print(f"Сервер слушает {host}:{port} (TCP)")

    while True:
        conn, addr = tcp_socket.accept()
        with conn:
            data = conn.recv(1024)
            if not data:
                continue
            try:
                a_str, b_str = data.decode("utf-8").split()
                a, b = float(a_str), float(b_str)
                c = math.sqrt(a*a + b*b)
                result = f"Гипотенуза c = {c}"
            except Exception as e:
                result = f"Ошибка: {e}"
            conn.sendall(result.encode("utf-8"))
