import socket

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Создаем TCP сокет на localhost и порт 9090

try:
    socket.connect(('localhost', 9090))  # Устанавливаем связь с сервером

    print("Введите 2 стороны прямоугольника через пробел")  # Получение данных с консоли
    try:
        data = str(input())
        socket.send(data.encode("utf-8"))

        result = socket.recv(1024).decode("utf-8")
        print("Результат = ", result)

    except Exception as e:
        print("Exception: ", e)

except Exception as e:
    print("Exception: ", e)

finally:
    socket.close()