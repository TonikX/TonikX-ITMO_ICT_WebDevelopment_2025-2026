import socket

HOST = 'localhost'
PORT = 8080
QUEUE = 10

def calculate_parallelogram_area(base, height):
    try:
        area = float(base) * float(height)
        return area
    except (ValueError, TypeError):
        return None

def tcp_server():
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    conn.bind((HOST, PORT))
    conn.listen(QUEUE)
    print(f"TCP сервер запущен на {HOST}:{PORT}")

    while True:
        try:
            clientsocket, addr = conn.accept()
            print(f"Подключился клиент: {addr}")
            
            data = clientsocket.recv(1024).decode('utf-8').strip()
            print(f"Получены данные: {data}")
            
            try:
                base, height = data.split()
                area = calculate_parallelogram_area(base, height)
                
                if area is not None:
                    response = f"Площадь параллелограмма: {area}"
                    print(f"Вычислена площадь: {area}")
                else:
                    response = "неверные параметры"
                    print("Ошибка в расчете")
                    
            except ValueError:
                response = "неверный формат данных"
                print("Ошибка формата данных")
            
            clientsocket.send(response.encode('utf-8'))
            print(f"Отправлен ответ: {response}")
            
            clientsocket.close()
            
        except KeyboardInterrupt:
            print("\nСервер остановлен")
            conn.close()
            break
        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    tcp_server()