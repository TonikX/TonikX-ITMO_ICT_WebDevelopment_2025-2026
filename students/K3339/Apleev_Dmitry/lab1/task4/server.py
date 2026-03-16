import socket
import threading

clients = []
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server_socket.bind(('localhost', 8885))
    server_socket.listen()
    print("Сервер чата запущен...")


    def handle_client(client_socket, addr):
        try:
            while True:
                msg = client_socket.recv(1024).decode('utf-8')
                if not msg:  # если клиент отключился
                    break

                print(f'Получено от {addr}: {msg}')
                for c in clients:
                    if c != client_socket:
                        try:
                            c.send(f'[{addr}] {msg}'.encode('utf-8'))
                        except:  # если какой-то клиент недоступен
                            continue

        except Exception as e:
            print(f"Ошибка с клиентом {addr}: {e}")

        finally:
            client_socket.close()
            if client_socket in clients:
                clients.remove(client_socket)
            print(f"Клиент {addr} отключен")


    while True:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)
        print(f'Новый клиент подключился: {addr}')
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

except Exception as e:
    print("Ошибка сервера:", e)

finally:
    server_socket.close()
    print("Сервер выключен")