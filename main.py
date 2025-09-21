#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Главный файл для запуска всех практических заданий
"""

import sys
import subprocess
import time
import threading

def print_menu():
    """Вывод главного меню"""
    print("Выберите задание для запуска:")
    print()
    print("1. Задание 1: UDP Hello")
    print("   Клиент отправляет серверу «Hello, server», сервер отвечает «Hello, client»")
    print()
    print("2. Задание 2: TCP Математические операции")
    print("   TCP сервер для выполнения математических вычислений")
    print("   - Теорема Пифагора")
    print("   - Квадратное уравнение")
    print("   - Площадь трапеции")
    print("   - Площадь параллелограмма")
    print()
    print("3. Задание 3: HTTP Сервер")
    print("   HTTP сервер, возвращающий HTML-страницу из файла")
    print()
    print("4. Задание 4: Многопользовательский чат")
    print("   TCP чат с поддержкой нескольких пользователей")
    print()
    print("5. Задание 5: Веб-сервер для оценок")
    print("   HTTP сервер для обработки GET и POST запросов")
    print()
    print("6. Запустить все задания (демонстрация)")
    print("0. Выход")
    print()

def run_task1():
    """Запуск задания 1"""
    print("\n=== ЗАДАНИЕ 1: UDP Hello ===")
    print("Запуск демонстрации UDP клиент-сервера...")
    subprocess.run([sys.executable, "task1_udp_hello.py", "demo"])

def run_task2():
    """Запуск задания 2"""
    print("\n=== ЗАДАНИЕ 2: TCP Математические операции ===")
    print("Запуск демонстрации TCP математического сервера...")
    subprocess.run([sys.executable, "task2_tcp_math.py", "demo"])

def run_task3():
    """Запуск задания 3"""
    print("\n=== ЗАДАНИЕ 3: HTTP Сервер ===")
    print("Запуск HTTP сервера...")
    print("Откройте http://localhost:8080/ в браузере")
    subprocess.run([sys.executable, "task3_http_server.py", "server"])

def run_task4():
    """Запуск задания 4"""
    print("\n=== ЗАДАНИЕ 4: Многопользовательский чат ===")
    print("Запуск чат сервера...")
    print("Для тестирования:")
    print("1. Запустите сервер: python task4_chat.py server")
    print("2. В другом терминале запустите клиент: python task4_chat.py client")
    print("3. Повторите шаг 2 для дополнительных клиентов")
    print("\nНажмите Enter для запуска сервера...")
    input()
    subprocess.run([sys.executable, "task4_chat.py", "server"])

def run_task5():
    """Запуск задания 5"""
    print("\n=== ЗАДАНИЕ 5: Веб-сервер для оценок ===")
    print("Запуск веб-сервера...")
    print("Откройте http://localhost:8081/ в браузере")
    subprocess.run([sys.executable, "task5_web_server.py"])

def run_all_demo():
    """Запуск демонстрации всех заданий"""
    
    tasks = [
        ("Задание 1: UDP Hello", run_task1),
        ("Задание 2: TCP Математика", run_task2),
        ("Задание 3: HTTP Сервер", run_task3),
        ("Задание 4: Многопользовательский чат", run_task4),
        ("Задание 5: Веб-сервер", run_task5)
    ]
    
    for i, (name, func) in enumerate(tasks, 1):
        print(f"\n--- {name} ---")
        try:
            func()
        except KeyboardInterrupt:
            print(f"\n{name} прерван пользователем")
        except Exception as e:
            print(f"\nОшибка в {name}: {e}")
        
        if i < len(tasks):
            print("\nНажмите Enter для перехода к следующему заданию...")
            input()
9
def main():
    """Главная функция"""

    while True:
        try:
            choice = input("Введите номер задания (0-6): ").strip().lower()
            
            if choice == '0':
                print("\nДо свидания!")
                break
            elif choice == '1':
                run_task1()
            elif choice == '2':
                run_task2()
            elif choice == '3':
                run_task3()
            elif choice == '4':
                run_task4()
            elif choice == '5':
                run_task5()
            elif choice == '6':
                run_all_demo()
            else:
                print("\\nНеверный выбор! Попробуйте снова.")
            
            if choice in ['1', '2', '3', '4', '5', '6']:
                print("\\n" + "="*60)
                input("Нажмите Enter для возврата в главное меню...")
                print()
                
        except KeyboardInterrupt:
            print("\\n\\nПрограмма прервана пользователем.")
            break
        except Exception as e:
            print(f"\\nОшибка: {e}")

if __name__ == "__main__":
    main()
