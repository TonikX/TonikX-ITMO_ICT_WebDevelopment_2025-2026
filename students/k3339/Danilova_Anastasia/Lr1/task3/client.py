# client.py
import socket


def http_client():
    HOST = 'localhost'
    PORT = 8090

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))

        http_request = """GET / HTTP/1.1
Host: localhost:8090
User-Agent: PythonSocketClient
Accept: text/html
Connection: close

"""
        client_socket.sendall(http_request.encode('utf-8'))

        response = b""
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            response += data

        response_str = response.decode('utf-8')

        headers, body = response_str.split('\r\n\r\n', 1)

        print("=== HTTP HEADERS ===")
        print(headers)

        print("\n=== HTML BODY ===")
        print(body)

    except ConnectionRefusedError:
        print('Error: Connection refused')
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    http_client()
