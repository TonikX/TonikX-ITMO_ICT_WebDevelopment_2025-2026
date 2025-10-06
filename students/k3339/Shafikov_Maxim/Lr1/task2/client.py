import socket
from students.k3339.Shafikov_Maxim.Lr1.config import host, port


if __name__ == "__main__":
    a = input("Введите катет a: ")
    b = input("Введите катет b: ")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(f"{a} {b}".encode("utf-8"))
        data = s.recv(1024)

    print("Ответ сервера:", data.decode("utf-8"))
