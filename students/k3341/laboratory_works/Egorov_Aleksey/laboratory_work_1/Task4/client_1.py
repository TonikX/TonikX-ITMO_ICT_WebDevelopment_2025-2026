import socket
import threading

HOST = '127.0.0.1'
PORT = 9090

nickname = input("Введите имя: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


def receive_message():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'nickname':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("Ошибка получения сообщения.")
            client.close()
            break


def write_message():
    while True:
        message = f"{nickname}: {input('')}"
        client.send(message.encode('utf-8'))


receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

write_thread = threading.Thread(target=write_message)
write_thread.start()
