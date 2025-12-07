import socket


def run_server(host: str = '127.0.0.1', port: int = 8080) -> None:
    '''
    Запуск UDP-сервера
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind((host, port))
        print(f'Server started at {host}:{port}')

        data, client_addr = server.recvfrom(1024)
        print(f'Recieved message from client: {data.decode()}')


        msg = 'Hello, client'
        server.sendto(msg.encode(), client_addr)
        print(f'Sended message to client {client_addr[0]}:{client_addr[1]}: {msg}')

if __name__ == '__main__':
    run_server()
