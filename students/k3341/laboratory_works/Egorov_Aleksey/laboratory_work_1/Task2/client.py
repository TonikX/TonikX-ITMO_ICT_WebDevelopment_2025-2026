import socket

HOST = '127.0.0.1'
PORT = 9090


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((HOST, PORT))
    except:
        print("Сервер недоступен.")
        return False

    print('Программа для расчёта площади трапеции')

    # Ввод параметров для запроса
    while True:
        try:
            low = input('Введите длину нижнего основания: ')
            high = input('Введите длину верхнего основания: ')
            height = input('Введите длину высоты: ')
            if all(value > 0 for value in map(float, (low, high, height))):
                break
            else:
                print('Все значения должны быть положительными!')
        except:
            print('Неверный формат данных')

    request = f'{low} {high} {height}'

    try:
        client_socket.sendall(request.encode('utf-8'))

        response = client_socket.recv(1024)
    except:
        print("Ошибка при запросе")

    print(f"Площадь трапеции: {response.decode('utf-8')}")

    client_socket.close()


if __name__ == '__main__':
    main()
