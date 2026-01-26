#!/usr/bin/env python3
"""
Задание 4: Многопользовательский чат (TCP с потоками)
Сервер поддерживает множество клиентов одновременно
"""

import socket
import threading

# Список подключенных клиентов
clients = []
clients_lock = threading.Lock()

def broadcast(message, sender_socket=None):
    """Отправляет сообщение всем подключенным клиентам, кроме отправителя"""
    with clients_lock:
        for client in clients:
            if client != sender_socket:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    # Если не удалось отправить, удаляем клиента
                    if client in clients:
                        clients.remove(client)

def handle_client(client_socket, client_address):
    """Обрабатывает сообщения от одного клиента"""
    print(f"[+] Новое подключение: {client_address}")
    
    # Запрашиваем имя пользователя
    try:
        client_socket.send("Введите ваше имя: ".encode('utf-8'))
        username = client_socket.recv(1024).decode('utf-8').strip()
        
        if not username:
            username = f"User_{client_address[1]}"
        
        # Добавляем клиента в список
        with clients_lock:
            clients.append(client_socket)
        
        # Уведомляем всех о новом пользователе
        join_message = f"\n[Сервер] {username} присоединился к чату!"
        print(join_message)
        broadcast(join_message, client_socket)
        
        # Приветствуем нового пользователя
        welcome_message = f"\nДобро пожаловать в чат, {username}!\nВсего пользователей онлайн: {len(clients)}\n"
        client_socket.send(welcome_message.encode('utf-8'))
        
        # Основной цикл получения сообщений
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                
                if not message:
                    break
                
                # Формируем и отправляем сообщение всем
                full_message = f"{username}: {message}"
                print(full_message)
                broadcast(full_message, client_socket)
                
            except ConnectionResetError:
                break
            except Exception as e:
                print(f"Ошибка при обработке сообщения от {username}: {e}")
                break
    
    except Exception as e:
        print(f"Ошибка при подключении клиента {client_address}: {e}")
    
    finally:
        # Удаляем клиента из списка
        with clients_lock:
            if client_socket in clients:
                clients.remove(client_socket)
        
        # Уведомляем всех об отключении
        if 'username' in locals():
            leave_message = f"\n[Сервер] {username} покинул чат."
            print(leave_message)
            broadcast(leave_message)
        
        # Закрываем соединение
        client_socket.close()
        print(f"[-] Отключение: {client_address}")

def main():
    # Создаем TCP сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Позволяем переиспользовать адрес
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Настройки сервера
    host = 'localhost'
    port = 9997
    
    # Привязываем сокет к адресу и порту
    server_socket.bind((host, port))
    
    # Начинаем прослушивание
    server_socket.listen(10)
    
    print("=" * 50)
    print(f"Многопользовательский чат-сервер запущен")
    print(f"Адрес: {host}:{port}")
    print("=" * 50)
    print("Ожидание подключений...\n")
    
    try:
        while True:
            # Принимаем подключение
            client_socket, client_address = server_socket.accept()
            
            # Создаем новый поток для обработки клиента
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address)
            )
            client_thread.daemon = True
            client_thread.start()
            
    except KeyboardInterrupt:
        print("\n\nОстановка сервера...")
    finally:
        # Закрываем все соединения
        with clients_lock:
            for client in clients:
                try:
                    client.close()
                except:
                    pass
        server_socket.close()
        print("Сервер остановлен")

if __name__ == "__main__":
    main()
