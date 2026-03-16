import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('localhost', 12345))
print("Сервер ждет сообщение...")
server_socket.settimeout(10)
try:
    while True:
        try:
            data, addr = server_socket.recvfrom(1024)
            print(f"Получено от клиента: {data.decode('utf-8')}")
            server_socket.sendto("Hi, client".encode('utf-8'), addr)
            print(f"Отправлен ответ {addr}: Hi, client")

        except socket.timeout:
            print("Превышено время ожидания")
            break

except Exception as e:
    print("Ошибка сервера:", e)

finally:
    server_socket.close()
    print("Сервер выключен")