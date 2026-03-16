import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', 12342))
server_socket.settimeout(20)
server_socket.listen()
print("Сервер запущен")

def solv (a,b,c):
    S=((a + b) * c / 2)
    return S

try:
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Подключился клиент{addr}")
        client_socket.settimeout(5)

        try:
            data = client_socket.recv(1024).decode('utf-8')
            print(f"получено от пользователя:{data} ")
            a, b, c = map(float, data.split(","))
            otv = solv(a,b,c)
            client_socket.send(str(round(otv, 2)).encode('utf-8'))
            print(f"Отправил пользователю:{otv} ")

        except socket.timeout:
            print("Превышено время ожидания данных, соединение закрыто")

        except Exception as e: #на всякий
            client_socket.send(f"Ошибка: {e}".encode('utf-8'))
            print(f"Отправил ошибку пользователю {e}")

        finally:
            client_socket.close()

except socket.timeout:
    print("Превышено время ожидания подключений, сервер выключен")

except Exception as e:
    print("Ошибка сервера:", e)

finally:
    server_socket.close()