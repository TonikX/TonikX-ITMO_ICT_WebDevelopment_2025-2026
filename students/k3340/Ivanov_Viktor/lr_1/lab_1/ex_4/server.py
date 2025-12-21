import socket
import threading
import json
import time
import unicodedata
from datetime import datetime

# параметры сервера
HOST = 'localhost'
PORT = 8083

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = {}  # {client_socket: {'username': str, 'address': tuple}}
        self.clients_lock = threading.Lock()
        self.running = False
    
    def clean_unicode(self, text):
        """Очистка текста от некорректных Unicode-символов"""
        if not isinstance(text, str):
            return text
        
        # Удаляем суррогатные символы
        cleaned = ''.join(char for char in text if not (0xD800 <= ord(char) <= 0xDFFF))
        
        # Нормализуем Unicode
        try:
            cleaned = unicodedata.normalize('NFKC', cleaned)
        except:
            pass
        
        return cleaned
        
    def start(self):
        """Запуск чат-сервера"""
        try:
            # создаем TCP сокет
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # привязываем сокет к адресу и порту
            self.server_socket.bind((self.host, self.port))
            
            # начинаем слушать входящие соединения
            self.server_socket.listen(10)
            self.running = True
            
            print(f"Многопользовательский чат-сервер запущен на {self.host}:{self.port}")
            print("Ожидание подключений клиентов...")
            print("Для остановки сервера нажмите Ctrl+C")
            
            # основной цикл принятия подключений
            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    print(f"Новое подключение от {client_address}")
                    
                    # создаем поток для обработки клиента
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except socket.error:
                    if self.running:
                        print("Ошибка при принятии подключения")
                    break
                    
        except Exception as e:
            print(f"Ошибка запуска сервера: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """Остановка чат-сервера"""
        print("\nОстановка чат-сервера...")
        self.running = False
        
        # закрываем все клиентские соединения
        with self.clients_lock:
            for client_socket in list(self.clients.keys()):
                try:
                    client_socket.close()
                except:
                    pass
            self.clients.clear()
        
        # закрываем серверный сокет
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        print("Чат-сервер остановлен")
    
    def handle_client(self, client_socket, client_address):
        """Обработка клиентского подключения в отдельном потоке"""
        username = None
        
        try:
            # получаем имя пользователя
            username_data = client_socket.recv(1024).decode('utf-8')
            if not username_data:
                return
            
            try:
                username_info = json.loads(username_data)
                username = self.clean_unicode(username_info.get('username', f'User_{client_address[1]}'))
            except json.JSONDecodeError:
                username = f'User_{client_address[1]}'
            
            # добавляем клиента в список
            with self.clients_lock:
                self.clients[client_socket] = {
                    'username': username,
                    'address': client_address,
                    'join_time': datetime.now()
                }
            
            # отправляем приветственное сообщение
            welcome_msg = {
                'type': 'system',
                'message': f'Добро пожаловать в чат, {username}!',
                'timestamp': datetime.now().isoformat(),
                'online_users': len(self.clients)
            }
            client_socket.sendall(json.dumps(welcome_msg, ensure_ascii=False).encode('utf-8'))
            
            # уведомляем всех о новом пользователе
            self.broadcast_message({
                'type': 'user_joined',
                'username': username,
                'message': f'{username} присоединился к чату',
                'timestamp': datetime.now().isoformat(),
                'online_users': len(self.clients)
            }, exclude_client=client_socket)
            
            print(f"{username} присоединился к чату (всего пользователей: {len(self.clients)})")
            
            # основной цикл получения сообщений от клиента
            while self.running:
                try:
                    data = client_socket.recv(1024).decode('utf-8')
                    if not data:
                        break
                    
                    # парсим сообщение
                    try:
                        message_data = json.loads(data)
                        message_type = message_data.get('type', 'message')
                        
                        if message_type == 'message':
                            # обычное сообщение
                            message = self.clean_unicode(message_data.get('message', ''))
                            if message.strip():
                                chat_message = {
                                    'type': 'message',
                                    'username': username,
                                    'message': message,
                                    'timestamp': datetime.now().isoformat()
                                }
                                self.broadcast_message(chat_message)
                                print(f"{username}: {message}")
                        
                        elif message_type == 'private':
                            # приватное сообщение
                            target_username = self.clean_unicode(message_data.get('target_username', ''))
                            message = self.clean_unicode(message_data.get('message', ''))
                            if target_username and message.strip():
                                self.send_private_message(username, target_username, message)
                        
                        elif message_type == 'session_request':
                            # запрос на приватную сессию
                            target_username = self.clean_unicode(message_data.get('target_username', ''))
                            if target_username:
                                self.request_private_session(username, target_username)
                        
                        elif message_type == 'session_response':
                            # ответ на запрос приватной сессии
                            target_username = self.clean_unicode(message_data.get('target_username', ''))
                            accepted = message_data.get('accepted', False)
                            if target_username:
                                self.handle_session_response(username, target_username, accepted)
                        
                        elif message_type == 'users':
                            # запрос списка пользователей
                            users_list = {
                                'type': 'users_list',
                                'users': [client_info['username'] for client_info in self.clients.values()],
                                'timestamp': datetime.now().isoformat()
                            }
                            client_socket.sendall(json.dumps(users_list, ensure_ascii=False).encode('utf-8'))
                    
                    except json.JSONDecodeError:
                        print(f"Ошибка парсинга JSON от {username}")
                        
                except socket.error:
                    break
                    
        except Exception as e:
            print(f"Ошибка обработки клиента {username or client_address}: {e}")
        
        finally:
            # удаляем клиента из списка
            with self.clients_lock:
                if client_socket in self.clients:
                    username = self.clients[client_socket]['username']
                    del self.clients[client_socket]
            
            # уведомляем всех о выходе пользователя
            if username:
                self.broadcast_message({
                    'type': 'user_left',
                    'username': username,
                    'message': f'{username} покинул чат',
                    'timestamp': datetime.now().isoformat(),
                    'online_users': len(self.clients)
                })
                print(f"{username} покинул чат (осталось пользователей: {len(self.clients)})")
            
            # закрываем соединение
            try:
                client_socket.close()
            except:
                pass
    
    def broadcast_message(self, message_data, exclude_client=None):
        """Отправка сообщения всем клиентам"""
        message_json = json.dumps(message_data, ensure_ascii=False).encode('utf-8')
        
        with self.clients_lock:
            disconnected_clients = []
            
            for client_socket, client_info in self.clients.items():
                if client_socket != exclude_client:
                    try:
                        client_socket.sendall(message_json)
                    except socket.error:
                        disconnected_clients.append(client_socket)
            
            # удаляем отключившихся клиентов
            for client_socket in disconnected_clients:
                try:
                    client_socket.close()
                except:
                    pass
                del self.clients[client_socket]
    
    def send_private_message(self, from_username, to_username, message):
        """Отправка приватного сообщения"""
        private_msg = {
            'type': 'private',
            'from_username': from_username,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        
        with self.clients_lock:
            for client_socket, client_info in self.clients.items():
                if client_info['username'] == to_username:
                    try:
                        client_socket.sendall(json.dumps(private_msg, ensure_ascii=False).encode('utf-8'))
                        print(f"Приватное сообщение от {from_username} к {to_username}: {message}")
                        return
                    except socket.error:
                        pass
        
        # если получатель не найден, отправляем ошибку отправителю
        error_msg = {
            'type': 'error',
            'message': f'Пользователь {to_username} не найден',
            'timestamp': datetime.now().isoformat()
        }
        
        with self.clients_lock:
            for client_socket, client_info in self.clients.items():
                if client_info['username'] == from_username:
                    try:
                        client_socket.sendall(json.dumps(error_msg, ensure_ascii=False).encode('utf-8'))
                        break
                    except socket.error:
                        pass
    
    def request_private_session(self, from_username, to_username):
        """Запрос на приватную сессию"""
        if from_username == to_username:
            # отправляем ошибку отправителю
            error_msg = {
                'type': 'error',
                'message': 'Нельзя создать сессию с самим собой',
                'timestamp': datetime.now().isoformat()
            }
            self.send_to_user(from_username, error_msg)
            return
        
        # отправляем запрос получателю
        session_request = {
            'type': 'session_request',
            'from_username': from_username,
            'message': f'{from_username} хочет начать приватную сессию с вами',
            'timestamp': datetime.now().isoformat()
        }
        
        if self.send_to_user(to_username, session_request):
            print(f"{from_username} запросил приватную сессию с {to_username}")
        else:
            # получатель не найден
            error_msg = {
                'type': 'error',
                'message': f'Пользователь {to_username} не найден',
                'timestamp': datetime.now().isoformat()
            }
            self.send_to_user(from_username, error_msg)
    
    def handle_session_response(self, responder_username, target_username, accepted):
        """Обработка ответа на запрос приватной сессии"""
        if accepted:
            # сессия принята - уведомляем обоих пользователей одинаковым сообщением
            success_msg = {
                'type': 'session_accepted',
                'from_username': target_username,
                'to_username': responder_username,
                'message': f'Приватная сессия между {target_username} и {responder_username} установлена',
                'timestamp': datetime.now().isoformat()
            }
            
            self.send_to_user(target_username, success_msg)
            self.send_to_user(responder_username, success_msg)
            
            print(f"{responder_username} принял приватную сессию с {target_username}")
        else:
            # сессия отклонена - уведомляем обоих пользователей одинаковым сообщением
            reject_msg = {
                'type': 'session_rejected',
                'from_username': target_username,
                'to_username': responder_username,
                'message': f'Приватная сессия между {target_username} и {responder_username} отклонена',
                'timestamp': datetime.now().isoformat()
            }
            
            self.send_to_user(target_username, reject_msg)
            self.send_to_user(responder_username, reject_msg)
            
            print(f"{responder_username} отклонил приватную сессию с {target_username}")
    
    def send_to_user(self, username, message_data):
        """Отправка сообщения конкретному пользователю"""
        message_json = json.dumps(message_data, ensure_ascii=False).encode('utf-8')
        
        with self.clients_lock:
            for client_socket, client_info in self.clients.items():
                if client_info['username'] == username:
                    try:
                        client_socket.sendall(message_json)
                        return True
                    except socket.error:
                        pass
            return False

def main():
    """Основная функция"""
    chat_server = ChatServer(HOST, PORT)
    
    try:
        chat_server.start()
    except KeyboardInterrupt:
        print("\nПолучен сигнал остановки...")
    finally:
        chat_server.stop()

if __name__ == "__main__":
    main()
