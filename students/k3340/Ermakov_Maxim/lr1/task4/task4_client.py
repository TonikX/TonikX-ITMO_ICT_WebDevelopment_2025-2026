import socket
import threading

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9092


def receive_messages_loop(client_socket):
    # Фоновый поток: постоянно получает строки от сервера и печатает их.
    client_file = client_socket.makefile("r", encoding="utf-8", newline="\n")
    try:
        for line in client_file:
            text_message = line.rstrip("\n")
            print(text_message)
    except Exception:
        pass
    finally:
        try:
            client_file.close()
        except Exception:
            pass


def main():
    user_name = input("Введите ваше имя: ").strip()
    if user_name == "":
        print("Имя не может быть пустым.")
        return

    # Создаём TCP-клиентский сокет и подключаемся к серверу
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
    except ConnectionRefusedError:
        print("Не удалось подключиться к серверу.")
        return

    # Сразу после подключения отправляем имя пользователя (одной строкой)
    try:
        client_socket.sendall((user_name + "\n").encode("utf-8"))
    except Exception as error:
        print(f"Ошибка при отправке имени: {error}")
        client_socket.close()
        return

    # Запускаем поток приёма сообщений, чтобы параллельно можно было вводить текст
    receiver_thread = threading.Thread(target=receive_messages_loop, args=(client_socket,), daemon=True)
    receiver_thread.start()

    # Основной цикл: читаем пользовательский ввод и отправляем на сервер
    try:
        while True:
            try:
                user_input = input()
            except EOFError:
                # На всякий случай, если stdin закрыт
                user_input = "/quit"

            if user_input.strip().lower() == "/quit":
                break

            # Отправляем строку на сервер
            try:
                client_socket.sendall((user_input + "\n").encode("utf-8"))
            except BrokenPipeError:
                print("Соединение с сервером потеряно.")
                break
            except Exception as error:
                print(f"Ошибка при отправке сообщения: {error}")
                break
    finally:
        try:
            client_socket.close()
        except Exception:
            pass
        print("Вы вышли из чата.")


if __name__ == "__main__":
    main()
