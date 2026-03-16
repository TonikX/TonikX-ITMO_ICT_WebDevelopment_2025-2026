import socket
import threading

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect(('localhost', 8885))


    def receive_messages(sock):
        while True:
            try:
                msg = sock.recv(1024).decode('utf-8')
                print(msg)
            except Exception as e:  # если сервер отключился
                print("Соединение разорвано \n")
                break

    thread = threading.Thread(target=receive_messages, args=(client_socket,))
    thread.start()
    print("Подключение к чату установлено")

    while True:
        try:
            msg = input()
            if msg == '/quit':
                print("Выход из чата")
                break
            client_socket.send(msg.encode('utf-8'))

        except KeyboardInterrupt:
            print("\nПринудительный выход")
            break

except Exception as e:
    print("Ошибка подключения:", e)

finally:
    client_socket.close()
    print("Клиент закрыт")