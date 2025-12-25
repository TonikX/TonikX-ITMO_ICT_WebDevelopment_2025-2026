import socket
import json
import threading
from chat.server_messages import CLIENT_SEND_ERROR
from chat.config import BUFFER_SIZE, ENCODING, HOST, PORT
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout


class Client:
    def __init__(self) -> None:
        self.name = input("Введите ваше имя: ")
        self.c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.c_socket.connect((HOST, PORT))
        self.give_name()

        # prompt_toolkit session
        self.session = PromptSession()

        # поток слушателя
        self.l_thread = threading.Thread(target=self.listen, daemon=True)
        self.l_thread.start()

        # основной цикл ввода prompt_toolkit
        self.run_input_loop()

    def give_name(self) -> None:
        try:
            server_request = json.loads(
                self.c_socket.recv(BUFFER_SIZE).decode(ENCODING)
            )
            if (
                isinstance(server_request, dict)
                and server_request["mes_type"] == "REG_NAME"
            ):
                name_mes = json.dumps({"name": self.name})
                self.send(name_mes)
            else:
                raise Exception
        except Exception as e:
            self.c_socket.close()
            print(e)


    def send(self, mes: str) -> None:
        try:
            self.c_socket.sendall(mes.encode(ENCODING))
        except Exception:
            print(CLIENT_SEND_ERROR)


    def listen(self):
        """Поток приёма сообщений. Выводит на экран всё, что пришло с сервера."""
        try:
            while True:
                data = self.c_socket.recv(BUFFER_SIZE)
                if not data:
                    break
                decoded = data.decode(ENCODING)
                # выводим только входящие сообщения
                if decoded[:len(self.name)] != self.name:
                    print(decoded)
        except Exception as e:
            self.c_socket.close()
            print(e)


    def run_input_loop(self):
        """Главный цикл ввода через prompt_toolkit (отправка сообщений)."""
        try:
            with patch_stdout():
                while True:
                    c_mes = self.session.prompt("> ")
                    if c_mes == "exit":
                        print("Завершаю соединение.")
                        self.c_socket.close()
                        break
                    if not c_mes.strip():
                        continue
                    self.send(c_mes)
        except Exception as e:
            self.c_socket.close()
            print(e)

