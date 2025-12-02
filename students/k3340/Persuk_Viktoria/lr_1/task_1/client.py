import socket


def run_client(server_host: str = '127.0.0.1', server_port: int = 8080):
    '''
    Запуск клиента и подключение с UDP-серверу
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        msg = 'Hello, server'

        client.sendto(msg.encode(), (server_host, server_port))
        print(f'Message send to server {server_host}:{server_port}: {msg}')

        data, _ = client.recvfrom(1024)
        print(f'Recieced response from server: {data.decode()}')


if __name__ == '__main__':
    run_client()
