import threading
import socket


def receive_message(client: socket.socket) -> None:
    '''
    Постоянно ждёт и получает сообщения от сервера
    Выводит сообщения пользователю
    Запускается в отдельном потоке
    client: клиентский сокет
    '''
    while True:
        try:
            msg = client.recv(1024)
            if not msg:
                print('Соединение с сервером разорвано')
                break
            print(f'{msg.decode("utf-8")}')
        except Exception:
            print('Ошибка при приёме сообщений')
            break


def run_client(server_host: str = 'localhost', server_port: int = 8080) -> None:
    '''
    Запуск клиента и подключение к многопользовательскому чату
    server_host: IP сервера
    server_port: порт сервера
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((server_host, server_port))
        print(f'Подключено к серверу {server_host}:{server_port}')

        # Присвоение и отправка на сервер ника пользователя
        nickname = input('Введите ваш никнейм: ')
        client.send(nickname.encode('utf-8'))

        # Запускаем отдельный поток для приёма сообщений от сервера
        threading.Thread(
            target=receive_message,
            args=(client,),
            daemon=True
        ).start()

        # Цикл для отправки сообщений на сервер в основном потоке
        while True:
            msg = input('>>> ')
            if msg.lower() == '/exit':
                # Выход из чата
                print('Выход из чата')
                break

            try:
                client.send(msg.encode('utf-8'))
            except Exception:
                print('Ошибка при отправке сообщения')
                break


if __name__ == '__main__':
    run_client()
