# server.py
import socket

HOST = '127.0.0.1'   
PORT = 9999          

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    print(f'UDP server listening on {HOST}:{PORT} ...')

    try:
        while True:
            data, addr = sock.recvfrom(1024)  
            msg = data.decode('utf-8')
            print(f'Received from {addr}: {msg}')

            
            if msg == 'Hello, server':
                reply = 'Hello, client'
            else:
                reply = 'Hello, client (reply)'

            sock.sendto(reply.encode('utf-8'), addr)
            print(f'Sent to {addr}: {reply}\n')
    except KeyboardInterrupt:
        print('\nServer stopped by user')
    finally:
        sock.close()

if __name__ == '__main__':
    main()
