import socket

HOST = "127.0.0.1"
PORT = 12345

menu = """
Выберите операцию:
1 - Теорема Пифагора (a, b)
2 - Квадратное уравнение (a, b, c)
3 - Площадь трапеции (a, b, h)
4 - Площадь параллелограмма (a, h)
"""

print(menu)
choice = int(input("Введите номер операции: "))

if choice == 1:
    a = float(input("Введите a: "))
    b = float(input("Введите b: "))
    request = f"{choice} {a} {b}"
elif choice == 2:
    a = float(input("Введите a: "))
    b = float(input("Введите b: "))
    c = float(input("Введите c: "))
    request = f"{choice} {a} {b} {c}"
elif choice == 3:
    a = float(input("Введите основание a: "))
    b = float(input("Введите основание b: "))
    h = float(input("Введите высоту h: "))
    request = f"{choice} {a} {b} {h}"
elif choice == 4:
    a = float(input("Введите сторону a: "))
    h = float(input("Введите высоту h: "))
    request = f"{choice} {a} {h}"
else:
    print("Неверный выбор")
    exit()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    client_socket.sendall(request.encode("utf-8"))
    data = client_socket.recv(1024).decode("utf-8")

print("Результат:", data)