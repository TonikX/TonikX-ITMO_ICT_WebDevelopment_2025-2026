import socket
import threading


def get_msg():
    while True:
        try:
            message = tcp_socket.recv(1024).decode('utf-8')
            if message == 'NICK':
                tcp_socket.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("Произошла ошибка")
            tcp_socket.close()
            break


def send_msg():
    while True:
        message = f'{nickname}: {input("")}'
        try:
            tcp_socket.sendall(message.encode('utf-8'))
        except:
            print("Не удалось отправить сообщение")
            break


# AF_INET - IPv4, SOCK_STREAM - TCP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr = ('localhost', 9999)

nickname = input("Выберите ваше имя: ")
tcp_socket.connect(addr)

receive_thread = threading.Thread(target=get_msg)
receive_thread.start()

write_thread = threading.Thread(target=send_msg)
write_thread.start()
