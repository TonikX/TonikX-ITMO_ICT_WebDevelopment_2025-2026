import socket
from datetime import datetime

def readPage(fileName="index.html"):
    try:
        with open(fileName, 'r', encoding="utf-8") as file:
            return file.read()

    except Exception as e:
        return f'<h1>Server Error: {e}</h1>'

def makeResponse(text):
    response = f"""
    HTTP/1.1 200 OK
    Date: {datetime.now()}
    Server: localhost
    Content-type:text/html; charset=UTF-8
    Content-Length: {len(text.encode("utf-8"))}
    
    {text} 
    """
    return response

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Создание TCP сокета
serverSocket.bind(('', 9090))
serverSocket.listen(3)
serverSocket.settimeout(60)

try:
    while True:
        clSocket, addr = serverSocket.accept()  # Устанавливаем соединение с клиентом

        try:
            request = clSocket.recv(1024).decode("utf-8")  # Читаем HTTP-запрос

            htmlText = readPage()  # Читаем страницу HTML

            http_response = makeResponse(htmlText)  # Формируем ответ

            clSocket.send(http_response.encode('utf-8'))  # Отправляем ответ

        except Exception as e:
            print("Exception: ", e)
            clSocket.send(f"""
            HTTP/1.1 500
            Error: {e} 
            """.encode('utf-8'))

        finally:
            clSocket.close()

except Exception as e:
    print("Exception: ", e)

finally:
    serverSocket.close()

