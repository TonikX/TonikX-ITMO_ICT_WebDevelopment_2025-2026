import socket


def load_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "<h1>404 - Not Found</h1>"
    except Exception as e:
        return "<h1>500 - Internal Server Error</h1>"


def create_http_response(content, status_code=200):
    status_messages = {
        200: "OK",
        404: "Not Found",
        500: "Internal Server Error"
    }
    response = f"HTTP/1.1 {status_code} {status_messages.get(status_code, 'Unknown')}\r\n"
    response += "Content-Type: text/html; charset=utf-8\r\n"
    response += "Content-Length: " + str(len(content)) + "\r\n"
    response += "\r\n"
    response += content
    return response


def main():
    HOST = '127.0.0.1'
    PORT = 8090

    html_content = load_file("index.html")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # REUSEADDR разрешает повторное использование порта
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.settimeout(1.0)  # 1 second

    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)

        print(f"Listening on http://{HOST}:{PORT}")
        print("Press Ctrl+C to stop the server...")

        running = True
        while running:
            try:
                client_socket, addr = server_socket.accept()
                print(f"Connection from {addr}")

                request = client_socket.recv(1024).decode()
                if request:
                    request_line = request.splitlines()[0]
                    method, path, _ = request_line.split()
                    print(f"Request Line: {request_line}")
                    print(f"Method: {method}")
                    print(f"Path: {path}")

                    http_response = create_http_response(html_content)
                    client_socket.sendall(http_response.encode('utf-8'))

                client_socket.close()

            except socket.timeout:
                continue

            except Exception as e:
                print(f"Error: {e}")
                if 'client_socket' in locals():
                    client_socket.close()

    except KeyboardInterrupt:
        print("\nServer is shutting down...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server_socket.close()
        print("Server stopped")


if __name__ == "__main__":
    main()
