import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 50002

def run_client():
    print('Клиент для вычислений по теореме Пифагора.')
    print('1) Вычислить гипотенузу по двум катетам')
    print('2) Вычислить катет по гипотенузе и другому катету')
    print('q) Выйти')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER_HOST, SERVER_PORT))
        
        while True:
            choice = input('Выберите опцию (1/2/q): ').strip().lower()
            if choice == 'q':
                message = 'quit'
            elif choice == '1':
                a = input('Введите катет a: ')
                b = input('Введите катет b: ')  
                message = f"hypotenuse {a} {b}"
            elif choice == '2':
                c = input('Введите гипотенузу c: ')
                known = input('Введите известный катет: ')
                message = f"leg {c} {known}"
            else:
                print('Неверный выбор. Попробуйте снова.')
                continue


            sock.sendall((message + "\n").encode("utf-8"))
            resp = sock.recv(1024).decode("utf-8").strip()
            print("Ответ сервера:", resp)
            if resp == "ok closing":
                break

if __name__ == "__main__":
    run_client()
