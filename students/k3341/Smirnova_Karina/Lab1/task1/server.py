import socket

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Создали сокет UDP
socket.bind(('', 9090))  # Соединили сокет с хостом '' и портом 9090
socket.settimeout(60)

try:
    while True:

        try:
            data, addr = socket.recvfrom(1024)  # Чтение данных от клиента
            print(data.decode("utf-8"))  # Печатаем декодированные данные
            socket.sendto("Hi, client".encode("utf-8"), addr)  # Отправляем ответ на адрес отправителя

        except socket.timeout:
            print("Socket timeout")
            break

        except Exception as e:
            print("Exception: ", e)
            continue

except Exception as e:
    print("Exception: ", e)
finally:
    socket.close()
