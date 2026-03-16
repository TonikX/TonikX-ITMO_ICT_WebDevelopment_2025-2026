import socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    clientSocket.connect(('localhost', 9091))
    http_request = """
    GET /index.html HTTP/1.1
    HOST: localhost 9090
    """
    clientSocket.send(http_request.encode('utf-8'))
    response = ''
    while True:
        part = clientSocket.recv(1024).decode('utf-8')
        if not part:
            break
        response += part
    print("Response:\n", response)
except Exception as e:
    print("Exception: ", e)
finally:
    clientSocket.close()