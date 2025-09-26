import socket
import threading

# Глобальная переменная для контроля работы
running = True

def receive_messages(client_socket):
    """Получает сообщения от сервера в отдельном потоке"""
    global running
    
    try:
        while running:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            # Принудительно очищаем буфер вывода для мгновенного отображения
            print(message, end='', flush=True)
            
    except Exception as e:
        if running:  # Показываем ошибку только если не закрываемся специально
            print(f"\n❌ Ошибка при получении сообщения: {e}", flush=True)
    finally:
        running = False

def start_client():
    """Запускает клиент чата"""
    global running
    
    # Создаем TCP сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Настройки подключения
    host = 'localhost'
    port = 12347
    
    try:
        # Подключаемся к серверу
        print("🔄 Подключение к серверу чата...")
        client_socket.connect((host, port))
        print("✅ Подключение установлено!")
        
        # Получаем запрос никнейма и отправляем его
        nickname_request = client_socket.recv(1024).decode('utf-8')
        print(nickname_request, end='', flush=True)
        
        nickname = input()
        client_socket.send(nickname.encode('utf-8'))
        
        # Получаем приветственное сообщение
        welcome = client_socket.recv(1024).decode('utf-8')
        print(welcome, end='', flush=True)
        
        # Запускаем поток для получения сообщений
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.daemon = True
        receive_thread.start()
        
        print("💬 Чат активен! Введите сообщение или 'exit' для выхода:", flush=True)
        print("-" * 50, flush=True)
        
        # Основной цикл отправки сообщений
        while running:
            try:
                message = input()
                
                if not running:
                    break
                    
                if message.lower() == 'exit':
                    break
                    
                if message.strip():  # Отправляем только непустые сообщения
                    client_socket.send(message.encode('utf-8'))
                    
            except EOFError:
                # Пользователь нажал Ctrl+D
                break
            except KeyboardInterrupt:
                # Пользователь нажал Ctrl+C
                print("\n🛑 Выход из чата...")
                break
                
    except ConnectionRefusedError:
        print("❌ Не удается подключиться к серверу. Убедитесь, что сервер запущен.")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        running = False
        client_socket.close()
        print("🔌 Соединение закрыто.")

if __name__ == "__main__":
    start_client()
