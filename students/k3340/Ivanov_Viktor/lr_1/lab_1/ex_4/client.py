import socket
import threading
import json
import time
import unicodedata
from datetime import datetime

# параметры сервера
HOST = 'localhost'
PORT = 8083

class ChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None
        self.username = None
        self.connected = False
        self.receive_thread = None
        # новые поля для режима сессии
        self.private_session = None  # Имя пользователя для приватной сессии
        self.session_active = False  # Активна ли приватная сессия
        # поля для обработки запросов сессий
        self.pending_session_request = None  # Ожидающий запрос на сессию
        self.session_response_thread = None  # Поток для обработки ответов на сессии
        self.waiting_for_session_response = False  # Ожидаем ли ответ на сессию
        self.session_request_from = None  # От кого запрос на сессию
    
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
        
    def connect(self, username):
        """подключение к чат-серверу"""
        try:
            # создаем TCP сокет
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # подключаемся к серверу
            self.client_socket.connect((self.host, self.port))
            
            # отправляем имя пользователя
            username_data = {
                'username': username
            }
            self.client_socket.sendall(json.dumps(username_data).encode('utf-8'))
            
            self.username = username
            self.connected = True
            
            print(f"\nПодключение к чат-серверу установлено!")
            print(f"Ваше имя: {username}")
            print("\nКоманды:")
            print("   /users - список пользователей")
            print("   /session username - начать приватную сессию")
            print("   /exit - выйти из приватной сессии")
            print("   /private username message - разовое приватное сообщение")
            print("   /quit - выход из чата")
            print(f"\nРежим: Общий чат")
            print("-" * 50)
            
            # запускаем поток для получения сообщений
            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.daemon = True
            self.receive_thread.start()
            
            return True
            
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            return False
    
    def disconnect(self):
        """Отключение от сервера"""
        self.connected = False
        
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
            self.client_socket = None
        
        print("Отключено от сервера")
    
    def receive_messages(self):
        """Получение сообщений от сервера в отдельном потоке"""
        while self.connected:
            try:
                data = self.client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                
                # парсим сообщение
                try:
                    message_data = json.loads(data)
                    self.display_message(message_data)
                except json.JSONDecodeError:
                    print(f"Ошибка парсинга сообщения: {data}")
                    
            except socket.error:
                if self.connected:
                    print("Соединение с сервером потеряно")
                break
            except Exception as e:
                if self.connected:
                    print(f"Ошибка получения сообщения: {e}")
                break
        
        self.connected = False
    
    def display_message(self, message_data):
        """Отображение полученного сообщения"""
        message_type = message_data.get('type', 'message')
        timestamp = message_data.get('timestamp', '')
        
        # форматируем время
        try:
            dt = datetime.fromisoformat(timestamp)
            time_str = dt.strftime("%H:%M:%S")
        except:
            time_str = timestamp
        
        if message_type == 'message':
            username = message_data.get('username', 'Unknown')
            message = message_data.get('message', '')
            print(f"\n[{time_str}] {username}: {message}")
            
        elif message_type == 'private':
            from_username = message_data.get('from_username', 'Unknown')
            message = message_data.get('message', '')
            print(f"\n[{time_str}] Приватно от {from_username}: {message}")
            
        elif message_type == 'system':
            message = message_data.get('message', '')
            online_users = message_data.get('online_users', 0)
            print(f"\n[{time_str}] {message} (Онлайн: {online_users})")
            
        elif message_type == 'user_joined':
            username = message_data.get('username', 'Unknown')
            online_users = message_data.get('online_users', 0)
            print(f"\n[{time_str}] {username} присоединился к чату (Онлайн: {online_users})")
            
        elif message_type == 'user_left':
            username = message_data.get('username', 'Unknown')
            online_users = message_data.get('online_users', 0)
            print(f"\n[{time_str}] {username} покинул чат (Онлайн: {online_users})")
            
        elif message_type == 'users_list':
            users = message_data.get('users', [])
            print(f"\n[{time_str}] Список пользователей онлайн:")
            for i, user in enumerate(users, 1):
                print(f"    {i}. {user}")
            print(f"Всего: {len(users)} пользователей")
            
        elif message_type == 'error':
            message = message_data.get('message', '')
            print(f"\n[{time_str}] Ошибка: {message}")
            
        elif message_type == 'session_request':
            from_username = message_data.get('from_username', 'Unknown')
            # устанавливаем флаг ожидания ответа на сессию
            self.waiting_for_session_response = True
            self.session_request_from = from_username
            print(f"\n{from_username} хочет начать приватную сессию с вами")
            print(f"Принять приватную сессию с {from_username}? (y/n): ", end='', flush=True)
                
        elif message_type == 'session_accepted':
            from_username = message_data.get('from_username', 'Unknown')
            to_username = message_data.get('to_username', 'Unknown')
            message = message_data.get('message', '')
            print(f"\n[{time_str}] {message}")
            
            # определяем, с кем у нас сессия
            if from_username == self.username:
                session_partner = to_username
            else:
                session_partner = from_username
            
            # автоматически переключаемся в приватную сессию
            self.private_session = session_partner
            self.session_active = True
            print(f"Режим: Приватная сессия с {session_partner}")
            
        elif message_type == 'session_rejected':
            from_username = message_data.get('from_username', 'Unknown')
            to_username = message_data.get('to_username', 'Unknown')
            message = message_data.get('message', '')
            print(f"\n[{time_str}] {message}")
            # остаемся в общем чате
            if self.session_active:
                self.exit_private_session()
    
    def send_message(self, message):
        """Отправка сообщения на сервер"""
        if not self.connected:
            print("Нет подключения к серверу")
            return False
        
        try:
            # Очищаем сообщение от некорректных Unicode-символов
            cleaned_message = self.clean_unicode(message)
            message_data = {
                'type': 'message',
                'message': cleaned_message
            }
            self.client_socket.sendall(json.dumps(message_data, ensure_ascii=False).encode('utf-8'))
            return True
        except Exception as e:
            print(f"Ошибка отправки сообщения: {e}")
            return False
    
    def send_private_message(self, target_username, message):
        """Отправка приватного сообщения"""
        if not self.connected:
            print("Нет подключения к серверу")
            return False
        
        try:
            # Очищаем сообщение от некорректных Unicode-символов
            cleaned_message = self.clean_unicode(message)
            cleaned_username = self.clean_unicode(target_username)
            message_data = {
                'type': 'private',
                'target_username': cleaned_username,
                'message': cleaned_message
            }
            self.client_socket.sendall(json.dumps(message_data, ensure_ascii=False).encode('utf-8'))
            print(f"\nПриватное сообщение отправлено пользователю {cleaned_username}")
            return True
        except Exception as e:
            print(f"\nОшибка отправки приватного сообщения: {e}")
            return False
    
    def request_users_list(self):
        """Запрос списка пользователей"""
        if not self.connected:
            print("Нет подключения к серверу")
            return False
        
        try:
            message_data = {
                'type': 'users'
            }
            self.client_socket.sendall(json.dumps(message_data).encode('utf-8'))
            return True
        except Exception as e:
            print(f"Ошибка запроса списка пользователей: {e}")
            return False
    
    def start_private_session(self, target_username):
        """Запрос на приватную сессию с пользователем"""
        if not self.connected:
            print("Нет подключения к серверу")
            return False
        
        # Очищаем имя пользователя
        cleaned_username = self.clean_unicode(target_username)
        
        if cleaned_username == self.username:
            print("Нельзя создать сессию с самим собой")
            return False
        
        # отправляем запрос на сервер
        session_request = {
            'type': 'session_request',
            'target_username': cleaned_username
        }
        
        try:
            self.client_socket.sendall(json.dumps(session_request, ensure_ascii=False).encode('utf-8'))
            print(f"\nЗапрос на приватную сессию с {cleaned_username} отправлен")
            print(f"Ожидание ответа...")
            return True
        except Exception as e:
            print(f"\nОшибка отправки запроса: {e}")
            return False
    
    def exit_private_session(self):
        """Выход из приватной сессии"""
        if not self.session_active:
            print("Приватная сессия не активна")
            return False
        
        print(f"\nВыход из приватной сессии с {self.private_session}")
        self.private_session = None
        self.session_active = False
        print(f"Режим: Общий чат")
        return True
    
    def get_prompt(self):
        """Получение текущего промпта для ввода"""
        if self.session_active:
            return f"[Приватно с {self.private_session}] "
        else:
            return "> "
    


def main():
    """Основная функция клиента"""
    print("=== Многопользовательский чат-клиент ===")
    print(f"Подключение к серверу: {HOST}:{PORT}")
    
    # получаем имя пользователя
    username = input("Введите ваше имя: ").strip()
    if not username:
        username = f"User_{int(time.time()) % 10000}"
        print(f"Используется имя по умолчанию: {username}")
    
    # создаем клиент
    chat_client = ChatClient(HOST, PORT)
    
    # подключаемся к серверу
    if not chat_client.connect(username):
        return
    
    try:
        # основной цикл ввода сообщений
        while chat_client.connected:
            try:
                # показываем текущий промпт
                prompt = chat_client.get_prompt()
                message = input(prompt).strip()
                
                if not message:
                    continue
                
                # обработка команд
                if message == '/quit':
                    print("Выход из чата...")
                    break
                    
                elif message == '/users':
                    chat_client.request_users_list()
                    continue
                    
                elif message.startswith('/session '):
                    # формат: /session username
                    parts = message.split(' ', 1)
                    if len(parts) >= 2:
                        target_user = parts[1]
                        chat_client.start_private_session(target_user)
                    else:
                        print("Формат: /session username")
                    continue
                    
                elif message == '/exit':
                    chat_client.exit_private_session()
                    continue
                    
                elif message.startswith('/private '):
                    # формат: /private username message
                    parts = message.split(' ', 2)
                    if len(parts) >= 3:
                        target_user = parts[1]
                        private_message = parts[2]
                        chat_client.send_private_message(target_user, private_message)
                    else:
                        print("Формат: /private username message")
                    continue
                
                # проверяем, ожидаем ли ответ на сессию
                if chat_client.waiting_for_session_response:
                    # обрабатываем ответ на сессию
                    accepted = message.lower() == 'y'
                    
                    # отправляем ответ на сервер
                    if chat_client.connected:
                        response_data = {
                            'type': 'session_response',
                            'target_username': chat_client.clean_unicode(chat_client.session_request_from),
                            'accepted': accepted
                        }
                        try:
                            chat_client.client_socket.sendall(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))
                        except:
                            pass
                    
                    if accepted:
                        print(f"\nПриватная сессия с {chat_client.session_request_from} принята!")
                        # автоматически переключаемся в приватную сессию
                        chat_client.private_session = chat_client.session_request_from
                        chat_client.session_active = True
                        print(f"Режим: Приватная сессия с {chat_client.session_request_from}")
                    else:
                        print(f"\nПриватная сессия с {chat_client.session_request_from} отклонена")
                    
                    # сбрасываем флаги
                    chat_client.waiting_for_session_response = False
                    chat_client.session_request_from = None
                    continue
                
                # отправка сообщения (обычного или приватного в зависимости от режима)
                if chat_client.session_active:
                    # в приватной сессии - отправляем приватное сообщение
                    if not chat_client.send_private_message(chat_client.private_session, message):
                        break
                else:
                    # в обычном режиме - отправляем общее сообщение
                    if not chat_client.send_message(message):
                        break
                    
            except KeyboardInterrupt:
                print("\nВыход из чата...")
                break
            except EOFError:
                break
                
    except Exception as e:
        print(f"Ошибка: {e}")
    
    finally:
        # отключаемся от сервера
        chat_client.disconnect()

if __name__ == "__main__":
    main()
