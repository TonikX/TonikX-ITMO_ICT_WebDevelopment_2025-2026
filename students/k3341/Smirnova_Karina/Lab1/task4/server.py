import socket
import threading

serverClients = list()  # Список клиентов


def sendMess(message, clSocket=None):
    # Отправляем сообщение всем, кроме автора
    for clientSocket, name in serverClients:
        if clientSocket != clSocket:
            try:
                clientSocket.send(message.encode('utf-8'))
            except Exception as e:
                print("Server Exception: ", e)
                removeClient(clientSocket)  # Удаляем клиента


def removeClient(clientSocket):
    for i, (sock, name) in enumerate(serverClients):
        if sock == clientSocket:
            serverClients.pop(i)
            try:
                sock.close()
            except Exception as e:
                print("Server Exception: ", e)
                pass

            print(f"Client {name} removed")
            sendMess(f'Client {name} gone')
            break


def meetClient(clSocket, address):
    try:
        name = clSocket.recv(1024).decode('utf-8')  # Получаем имя клиента для приветствия
        print(f"Client {name} added from address: {address}")

        serverClients.append((clSocket, name))  # Запоминаем клиента
        sendMess(f'Client {name} added in chat.', clSocket)  # Отправляем всем сообщение о подключении клиента

        # Читаем сообщения
        while True:
            try:

                message = clSocket.recv(1024).decode('utf-8')

                if not message:
                    break

                readyMessage = f'{name}: {message}'
                sendMess(readyMessage, clSocket)

            except Exception as e:
                print("Server Exception: ", e)
                break

    except Exception as e:
        print("Server Exception: ", e)
        clSocket.sendto(("Can't add you in chat. Exception: " + str(e)).encode('utf-8'))


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Создаем сокет localhost 9090
serverSocket.bind(('', 9090))
serverSocket.listen(5)
serverSocket.settimeout(180)
print("Server is ready for work")

try:
    while True:
        clSocket, addr = serverSocket.accept()  # Принимаем подключение
        clientThread = threading.Thread(target=meetClient, args=(clSocket, addr),
                                        daemon=True)  # Создаем поток для подключенного клиента
        clientThread.start()

except Exception as e:
    print("Server Exception: ", e)

finally:
    for clSocket, name in serverClients:
        try:
            clSocket.close()
        except:
            pass
    serverSocket.close()
    print("Server stopped")
