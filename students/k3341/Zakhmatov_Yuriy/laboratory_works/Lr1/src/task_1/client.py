import socket

def run():
    #Создаем сокет для клиента UDP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        #Подключаемся к сокету
        client_socket.connect(('localhost', 8080))

        #Отправляем сообщение
        client_socket.sendall(b'Hello, server')

        #Получаем ответ
        response = client_socket.recv(1024)
        print(f"Response from server: {response.decode('utf-8')}")
    except Exception as e:
        print(e)
    finally:
        client_socket.close()

if __name__ == '__main__':
    run()