import socket      # Модуль для работы с сетевыми сокетами
import threading   # Модуль для работы с потоками

def process_recieve(sock_client):  
    # Функция для постоянного получения сообщений от сервера
    while True:  
        response = sock_client.recv(1024).decode()  
        # Получаем до 1024 байт и декодируем в строку
        print(response)  
        # Выводим сообщение на экран

sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
# Создаем TCP-сокет для клиента

sock_client.connect(('localhost', 8080))  
# Подключаемся к серверу по адресу localhost:8080

name = input("Name: ")  
# Просим пользователя ввести своё имя

thr = threading.Thread(target=process_recieve, args=(sock_client,))  
# Создаем поток для функции получения сообщений (чтобы принимать и печатать одновременно)
thr.start()  
# Запускаем поток

print("You join to chat")  
# Сообщение о подключении к чату

while True:  
    text = input()  
    # Ждем ввод текста от пользователя
    sock_client.sendall((name + ": " + text).encode())  
    # Отправляем введённое сообщение на сервер в виде "имя: сообщение"