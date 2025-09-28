import socket
import threading

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 50004

def processing_user_input(socket):
    while True:
        try:
            message = input('').strip()
            if message=='quit':
                break
            socket.sendall((message + "\0").encode("utf-8"))
        except:
            break

def processing_input_messages(socket):
    while True:
        try:
            resp = socket.recv(1024).decode("utf-8").strip()
            print("Полученно сообщение:", resp)
        except:
            break

def run_client():
    print('Клиент чата запущен')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER_HOST, SERVER_PORT))

        thread_user_input = threading.Thread(target=processing_user_input, args=[sock])
        thread_user_input.start()
        thread_input_messages = threading.Thread(target=processing_input_messages, args=[sock])
        thread_input_messages.start()

        while thread_user_input.is_alive() and thread_input_messages.is_alive():
            pass

        # while processing_user_input(sock) and thread_input_messages.is_alive():
        #     pass

if __name__ == "__main__":
    run_client()
