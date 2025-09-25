import socket


def run_client(server_host: str = '127.0.0.1', server_port: int = 8080):
    '''
    Запуск клиента и подключение к TCP серверу
    '''

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((server_host, server_port))

        a = input('Значение катета a (или пусто): ')
        b = input('Значение катета b (или пусто): ')
        c = input('Значение гипотенузы c (или пусто): ')

        params = ','.join([a, b, c])
        client.sendall(params.encode())

        data = client.recv(1024)
        print(f'Результат от сервера: {data.decode()}')


if __name__ == '__main__':
    run_client()
