import socket

HOST = '127.0.0.1'
PORT = 8003
ENCODING = 'utf-8'

def main():
    print("🌐 HTTP Клиент")
    print("=" * 15)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"✅ Подключен к серверу {HOST}:{PORT}")

        request = "GET / HTTP/1.1\r\n"
        request += f"Host: {HOST}:{PORT}\r\n"
        request += "Connection: close\r\n\r\n"
        
        s.sendall(request.encode(ENCODING))
        print("📤 Отправлен GET запрос")

        response = b""
        while True:
            data = s.recv(1024)
            if not data:
                break
            response += data

        response_text = response.decode(ENCODING)
        if '\r\n\r\n' in response_text:
            headers, body = response_text.split('\r\n\r\n', 1)
            print("\n📥 HTTP заголовки:")
            print("-" * 30)
            print(headers)
            print("\n📄 HTML содержимое:")
            print("-" * 30)
            print(body)
        else:
            print("\n📥 Получен ответ:")
            print(response_text)

if __name__ == '__main__':
    main()
