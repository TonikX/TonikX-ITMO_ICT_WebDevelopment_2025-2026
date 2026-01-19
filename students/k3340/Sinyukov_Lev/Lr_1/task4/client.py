import socket
import threading

def recieve_message(client_sock):
    while True:
        try:
            message = client_sock.recv(1024).decode("utf-8")
            if message:
                print(message)
        except:
            print('No server connection')
            client_sock.close()
            break

def func_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    thread = threading.Thread(target=recieve_message, args=(client_socket,))
    thread.start()

    while True:
        message = input()
        client_socket.send(message.encode("utf-8"))

HOST = 'localhost'
PORT = 8080

func_client()