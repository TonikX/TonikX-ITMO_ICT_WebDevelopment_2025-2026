import socket


def parallelogram_area(base, height):
    return base * height


HOST = 'localhost'
PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)
print("[TCP] Server is running on port {}".format(PORT))

while True:
    conn, addr = sock.accept()
    print(f"Подключен клиент: {addr}")
    try:
        data = conn.recv(1024).decode()
        if not data:
            continue

        params = data.split(',')

        base, height = map(float, params)
        result = parallelogram_area(base, height)
        conn.send(str(result).encode())
    except Exception as e:
        conn.send(f"Ошибка: {e}".encode())
    finally:
        conn.close()
