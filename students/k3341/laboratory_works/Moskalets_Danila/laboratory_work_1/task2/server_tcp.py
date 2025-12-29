import socket

HOST = '127.0.0.1'
PORT = 9090

# создаем tcp пакет: SOCK_STREAM - tcp
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)  # ждем подключения одного клиента

print(f"Сервер запущен на {HOST}:{PORT}")
conn, addr = server_socket.accept()  # ждем подключение
print(f"Подключен клиент: {addr}")

while True:
    data = conn.recv(1024).decode()  # получаем данные
    if not data:
        break
    try:
        a, b, h = map(float, data.split())
        area = ((a + b) / 2) * h
        conn.send(f"Площадь трапеции = {area}".encode())
    except:
        conn.send("Ошибка: введите три числа через пробел".encode())

conn.close()
server_socket.close()