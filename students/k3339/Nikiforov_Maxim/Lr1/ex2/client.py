import socket
import sys

HOST = 'localhost'
PORT = 8080

def require_pos(x, name):
    if x <= 0:
        print(f"Ошибка: {name} должно быть > 0.")
        sys.exit(1)

# 1) Берём номер в журнале и вычисляем вариант
try:
    n = int(input("Введите ваш номер в журнале (целое > 0): ").strip())
    if n <= 0:
        print("Ошибка: номер должен быть > 0.")
        sys.exit(1)
except ValueError:
    print("Ошибка: номер должен быть целым числом.")
    sys.exit(1)

variant = ((n - 1) % 4) + 1
print(f"Ваш вариант: {variant}")

# 2) Спрашиваем только нужные параметры и формируем сообщение
try:
    if variant == 1:
        # Теорема Пифагора
        a = float(input("a (катет 1): "))
        b = float(input("b (катет 2): "))
        require_pos(a, "a")
        require_pos(b, "b")
        msg = f"PYTH {a} {b}\n"

    elif variant == 2:
        # Квадратное уравнение (коэффициенты любые)
        a = float(input("a: "))
        b = float(input("b: "))
        c = float(input("c: "))
        msg = f"QUAD {a} {b} {c}\n"

    elif variant == 3:
        # Площадь трапеции
        a = float(input("a (основание 1): "))
        b = float(input("b (основание 2): "))
        h = float(input("h (высота): "))
        require_pos(a, "a")
        require_pos(b, "b")
        require_pos(h, "h")
        msg = f"TRAP {a} {b} {h}\n"

    else:  # variant == 4
        # Площадь параллелограмма
        a = float(input("a (сторона/основание): "))
        h = float(input("h (высота): "))
        require_pos(a, "a")
        require_pos(h, "h")
        msg = f"PARA {a} {h}\n"

except ValueError:
    print("Ошибка: параметры должны быть числами.")
    sys.exit(1)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
sock.sendall(msg.encode('utf-8'))

data = sock.recv(1024)
print("Ответ сервера:", data.decode('utf-8', errors='ignore').strip())

sock.close()

