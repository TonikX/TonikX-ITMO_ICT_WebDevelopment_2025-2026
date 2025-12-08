import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9091

# Просим пользователя ввести данные с клавиатуры
print("Введите параметры параллелограмма")
a = input("Введите основание a: ").strip()
h = input("Введите высоту h: ").strip()

# Формируем запрос
request = f"{a} {h}"

# Создаём TCP-сокет, подключаемся к серверу и отправляем запрос
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    client_socket.sendall(request.encode("utf-8"))

    #  Получаем ответ
    data = client_socket.recv(1024)
    reply = data.decode("utf-8").strip()

    print(f"Ответ от сервера: {reply}")

except ConnectionRefusedError:
    print("Не удалось подключиться к серверу.")
finally:
    client_socket.close()
