import socket
import threading

nickname = input('Choose your nickname: ').strip() or 'Anonymous'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9555))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if not message:
                print('[Disconnected from server]')
                break
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message, end='' if message.endswith('\n') else '\n')
        except:
            print('An error occurred. Closing connection.')
            client.close()
            break
def write():
    while True:
        try:
            text = input()
        except EOFError:
            break
        try:
            client.send(text.encode('utf-8'))
        except:
            break


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
