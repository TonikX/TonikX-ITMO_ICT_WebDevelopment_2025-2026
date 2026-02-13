import socket

# Создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключаемся к серверу
client_socket.connect(('localhost', 8911))
print("Подключение к серверу установлено")

first_response = client_socket.recv(1024)
print(first_response.decode())

while True:
    ans = input("Введите коэффициенты (или 'exit' для выхода): ")

    if ans.lower() == 'exit':
        print("Завершение работы...")
        break

    client_socket.sendall(ans.encode())

    # Получаем ответ от сервера
    response = client_socket.recv(1024).decode()
    print(f'Ответ от сервера: {response}')

client_socket.close()