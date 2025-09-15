import socket
import math

def solvePifagor(a, b):
    return math.sqrt(a**2 + b**2)

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Создаем TCP сокет на localhost и порт 9090
socket.bind(('', 9090))
socket.settimeout(60)
socket.listen(3)

try:
    while True:
        clSocket, addr = socket.accept()  # Принимаем соединение

        try:
            data = clSocket.recv(1024).decode("utf-8")
            a, b = map(int, data.split(" "))
            res = solvePifagor(a, b)
            clSocket.send(str(res).encode("utf-8"))

        except Exception as e:
            clSocket.send(("Exception: " + str(e)).encode("utf-8"))

        finally:
            clSocket.close()

except Exception as e:
    print("Exception: ", e)

finally:
    socket.close()