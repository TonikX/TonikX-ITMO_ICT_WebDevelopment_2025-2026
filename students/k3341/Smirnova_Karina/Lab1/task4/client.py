import socket, threading

def receiveMessage(clientSocket):
    while True:
        try:
            message = clientSocket.recv(1024).decode('utf-8')

            if not message:
                print('No message')
                break

            print(message, flush=True)

        except Exception as e:
            print("Exception: ", e)

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    clientSocket.connect(('localhost', 9090))

    name = str(input("Введите свое имя:"))
    clientSocket.send(name.encode('utf-8'))

    # Поток для получения сообщений
    receiveThread = threading.Thread(target=receiveMessage, args=(clientSocket,), daemon=True)
    receiveThread.start()

    # Отправка сообщений
    while True:
        try:
            message = str(input())

            # Выход из чата
            if message == '':
                break

            clientSocket.send(message.encode('utf-8'))

        except Exception as e:
            print("Exception: ", e)
            break

except Exception as e:
    print("Client Exception: ", e)

finally:
    clientSocket.close()