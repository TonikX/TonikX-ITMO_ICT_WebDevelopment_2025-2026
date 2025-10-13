# server.py
import socket

HOST = '127.0.0.1'   
PORT = 8080          

def main():
    
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    
    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type: text/html; charset=utf-8\r\n"
    response += f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
    response += "Connection: close\r\n"
    response += "\r\n"  
    response += html_content

    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print(f"HTTP server running on http://{HOST}:{PORT}")

    try:
        while True:
            conn, addr = server_socket.accept()
            print(f"Client connected: {addr}")

            
            request = conn.recv(1024).decode("utf-8")
            print(f"Request:\n{request}\n")

            
            conn.sendall(response.encode("utf-8"))
            conn.close()
    except KeyboardInterrupt:
        print("Server stopped")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
