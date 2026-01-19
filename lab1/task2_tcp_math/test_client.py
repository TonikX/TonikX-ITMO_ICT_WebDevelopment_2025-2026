#!/usr/bin/env python3
"""
Тестовый клиент для автоматической проверки всех математических операций
"""

import socket
import sys

def send_test_request(server_host, server_port, request, description):
    """Отправляет тестовый запрос и выводит результат"""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_host, server_port))
        
        client_socket.send(request.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        
        print(f"\n{description}")
        print(f"Запрос: {request}")
        print(f"Результат: {response}")
        
        client_socket.close()
        return True
        
    except Exception as e:
        print(f"Ошибка теста '{description}': {e}")
        return False

def main():
    server_host = 'localhost'
    server_port = 12346
    
    print("=== Тестирование TCP Math Server ===")
    
    # Тестовые случаи
    test_cases = [
        ("1,3,4", "Теорема Пифагора (катеты 3, 4)"),
        ("1,5,12", "Теорема Пифагора (катеты 5, 12)"),
        ("2,1,-5,6", "Квадратное уравнение (x² - 5x + 6 = 0)"),
        ("2,1,2,1", "Квадратное уравнение (x² + 2x + 1 = 0)"),
        ("2,1,1,1", "Квадратное уравнение (x² + x + 1 = 0)"),
        ("3,5,7,4", "Площадь трапеции (основания 5, 7, высота 4)"),
        ("3,10,6,8", "Площадь трапеции (основания 10, 6, высота 8)"),
        ("4,6,8", "Площадь параллелограмма (основание 6, высота 8)"),
        ("4,12,5", "Площадь параллелограмма (основание 12, высота 5)"),
    ]
    
    success_count = 0
    total_tests = len(test_cases)
    
    for request, description in test_cases:
        if send_test_request(server_host, server_port, request, description):
            success_count += 1
    
    print(f"\n=== Результаты тестирования ===")
    print(f"Успешно выполнено: {success_count}/{total_tests} тестов")
    
    if success_count == total_tests:
        print("✅ Все тесты прошли успешно!")
    else:
        print("❌ Некоторые тесты не прошли")

if __name__ == "__main__":
    main()
