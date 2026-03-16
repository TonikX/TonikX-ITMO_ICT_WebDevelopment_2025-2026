import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(5)

try:
    mes = input("Введите сообщение для  сервера: ")
    client_socket.sendto(mes.encode('utf-8'), ('localhost', 12345))
    data, addr = client_socket.recvfrom(1024)
    print(f"Ответ от сервера: {data.decode('utf-8')}")
    client_socket.close()

except socket.timeout: #если сервер не робит
    print("Превышено время ожидания ответа")

except Exception as e:
    print("Ошибка:", e)
finally:
    client_socket.close()