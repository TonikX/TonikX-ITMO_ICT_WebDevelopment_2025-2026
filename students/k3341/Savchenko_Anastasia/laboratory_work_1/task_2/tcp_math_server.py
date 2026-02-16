import socket


def calculate_area(base, height):
    return base * height


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 1235))
server.listen(1)

while True:
    conn, _ = server.accept()
    data = conn.recv(1024).decode()

    base, height = map(float, data.split())
    area = calculate_area(base, height)

    conn.send(str(area).encode())
    conn.close()

# === Вычисление площади параллелограмма ===
# Формула: S = a * h
# где a - основание, h - высота