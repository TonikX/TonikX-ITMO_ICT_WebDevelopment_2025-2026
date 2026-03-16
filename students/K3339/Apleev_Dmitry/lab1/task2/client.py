import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect(('localhost', 12342))

    while True:
        try:
            a = float(input("Основание a: "))
            b = float(input("Основание b: "))
            c = float(input("Высота c: "))
            break

        except ValueError:
            print("Ошибка! Введите числа заново.")

    client_socket.send(f"{a},{b},{c}".encode('utf-8'))
    result = client_socket.recv(1024).decode('utf-8')
    print("Площадь трапеции:", result)

except Exception as e:
    print("Ошибка:", e)
finally:
    client_socket.close()