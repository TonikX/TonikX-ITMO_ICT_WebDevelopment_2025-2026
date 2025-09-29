import socket
import math

HOST = "localhost"
PORT = 9090

# Создаем TCP-сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)  # макс. 1 клиент в очереди

print(f"TCP сервер запущен на {HOST}:{PORT}...")

while True:
    conn, addr = server_socket.accept()
    print(f"Подключение от {addr}")

    # Получаем данные от клиента
    data = conn.recv(1024).decode()
    if not data:
        conn.close()
        continue

    # Данные приходят как "a b"
    try:
        a_str, b_str = data.split()
        a, b = float(a_str), float(b_str)
        c = math.sqrt(a**2 + b**2)
        result = f"Гипотенуза: {c:.2f}"
    except Exception as e:
        result = f"Ошибка вычислений: {e}"

    # Отправляем результат клиенту
    conn.sendall(result.encode())

    conn.close()
