import socket

HOST = "127.0.0.1"
PORT = 12345

print("Выберите операцию:")
print("1. Теорема Пифагора (a, b)")
print("2. Решение квадратного уравнения (a, b, c)")
print("3. Площадь трапеции (a, b, h)")
print("4. Площадь параллелограмма (a, h)")

choice = input("Введите номер операции: ")

if choice == "1":
    a = float(input("Введите a: "))
    b = float(input("Введите b: "))
    message = f"{choice} {a} {b}"

elif choice == "2":
    a = float(input("Введите a: "))
    b = float(input("Введите b: "))
    c = float(input("Введите c: "))
    message = f"{choice} {a} {b} {c}"

elif choice == "3":
    a = float(input("Введите a: "))
    b = float(input("Введите b: "))
    h = float(input("Введите h: "))
    message = f"{choice} {a} {b} {h}"

elif choice == "4":
    a = float(input("Введите a: "))
    h = float(input("Введите h: "))
    message = f"{choice} {a} {h}"

else:
    print("Некорректный выбор!")
    exit()

# Создаём TCP-сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Отправляем запрос
client_socket.send(message.encode())

# Получаем результат
result = client_socket.recv(1024).decode()
print("Результат от сервера:", result)

client_socket.close()
