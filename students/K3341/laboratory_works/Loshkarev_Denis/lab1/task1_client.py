import socket

HOST = '127.0.0.1'
PORT = 8888

BUFFER_SIZE = 1024

def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        message = "Hello, server"
        
        # UDP не требует предварительного connect(), адрес указывается в sendto()
        s.sendto(message.encode('utf-8'), (HOST, PORT))
        print(f"Отправлено серверу: **{message}**")
        

        data, addr = s.recvfrom(BUFFER_SIZE)
        
        received_response = data.decode('utf-8')
        print("-" * 30)
        print(f"Получен ответ от {addr}: **{received_response}**")
        print("-" * 30)

if __name__ == '__main__':
    run_client()