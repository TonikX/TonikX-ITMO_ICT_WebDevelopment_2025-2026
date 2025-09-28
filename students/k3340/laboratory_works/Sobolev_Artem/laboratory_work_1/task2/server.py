import socket
import math

SERVER_ADDRESS = ("127.0.0.1", 10000)

def main():
    # socket.SOCK_STREAM указывает, что это TCP-сокет
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Позволяем запускать сервер на том же порту
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(SERVER_ADDRESS)
        server_socket.listen()

        while True:
            # При подключении клиента создаётся отдельный сокет conn
            conn, addr = server_socket.accept()
            try:
                # Принимаем сообщение от клиента
                data = conn.recv(1024)
                if not data:
                    continue
                values = list(map(float, data.decode("utf-8", errors="replace").split()))
                if len(values) != 2 or not(values[0] > 0 and values[1] > 0):
                    raise ValueError
            except ValueError:
                conn.sendall("Необходимо передать 2 положительных числа через пробел".encode("utf-8"))
                continue
            else:
                result = math.hypot(*values)
                message = f"Гипотенуза треугольника со сторонами {values[0]} и {values[1]} равна {result}"
                # Отправляем сообщение
                conn.sendall(message.encode())
            finally:
                conn.close()

if __name__ == "__main__":
    main()