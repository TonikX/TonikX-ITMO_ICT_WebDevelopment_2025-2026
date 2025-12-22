import socket

HOST = '127.0.0.1' 
PORT = 8888

BUFFER_SIZE = 1024

def run_server():
    # AF_INET - семейство адресов IPv4
    # SOCK_DGRAM - тип сокета (UDP)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # привязка сокета к адресу и порту
        s.bind((HOST, PORT))
        print(f"UDP Сервер запущен на {HOST}:{PORT}")
        print("Ожидание данных...")

        # data - сообщение, addr - адрес клиента
        data, addr = s.recvfrom(BUFFER_SIZE)
        
        # Декодируем полученное сообщение
        received_message = data.decode('utf-8')
        print("-" * 30)
        print(f"Получено от {addr}: **{received_message}**")
        
        # Отправка ответа
        response_message = "Hello, client"
        s.sendto(response_message.encode('utf-8'), addr)
        print(f"Отправлено клиенту {addr}: **{response_message}**")
        print("-" * 30)

if __name__ == '__main__':
    run_server()