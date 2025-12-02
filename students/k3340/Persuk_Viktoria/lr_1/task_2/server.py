import socket
from math import sqrt
from typing import Tuple


# 1 вариант
def calculate_pythagorean(
        a: float | None = None,
        b: float | None = None,
        c: float | None = None
        ) -> Tuple[float, float] | bool:
    '''
    Подсчёт значений катетов/гипотенузы по теореме Пифагора
    с переменным количеством переменных (минимум 2 не None)
    '''
    count_arguments = sum(x is None for x in (a, b, c))
    if count_arguments >= 2:
        raise ValueError('Должно быть передано как минимум 2 аргумента')

    # 3 случая рассматриваем
    if (a is not None) and (b is not None) and (c is None):
        # даны только a и b
        c = sqrt(a ** 2 + b ** 2)
        c_squared = c ** 2
        return ((c_squared, c))

    elif ((a is not None) and (b is None) and (c is not None)) or \
        ((a is None) and (b is not None) and (c is not None)):
        # даны только a и c
        if b is None:
            b = a

        a = round(sqrt(c ** 2 - b ** 2), 2)
        a_squared = round(a ** 2, 2)
        return ((a_squared, a))

    else:
        # даны a, b и c
        return True if ((a ** 2 + b ** 2) == (c ** 2)) else False


def run_server(server_host: str = '127.0.0.1', server_port: int = 8080):
    '''Запуск TCP-сервера'''

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((server_host, server_port))
        server.listen(1)
        print(f'Сервер слушает на {server_host}:{server_port}')
        conn, addr = server.accept()

        with conn:
            print(f'Подключено клиентом {addr}')
            data = conn.recv(1024)

            if data:
                params = data.decode().split(',')
                a, b, c = [int(x) if x else None for x in params]

                try:
                    result = calculate_pythagorean(a, b, c)
                except Exception as e:
                    conn.sendall(f'Ошибка: {e}'.encode())
                else:
                    conn.sendall(str(result).encode())


if __name__ == '__main__':
    run_server()
