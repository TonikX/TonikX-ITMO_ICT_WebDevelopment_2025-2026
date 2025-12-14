#!/usr/bin/env python
"""
Скрипт для добавления дополнительных тестовых данных для проверки пагинации
"""
import os
import sys
import django
from datetime import date, datetime, timedelta
from django.utils import timezone

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homework_board.settings')
django.setup()

from assignments.models import User, Subject, Assignment, Submission, Grade

def add_more_assignments():
    """Добавление дополнительных заданий для тестирования пагинации"""
    
    # Получаем существующие предметы и преподавателей
    subjects = list(Subject.objects.all())
    teachers = list(User.objects.filter(role=User.TEACHER))
    
    if not subjects or not teachers:
        print("Ошибка: Нет предметов или преподавателей. Сначала запустите populate_data.py")
        return
    
    # Создаем дополнительные задания
    additional_assignments = [
        {
            'subject': subjects[0],  # Математика
            'teacher': teachers[0],
            'title': "Дифференциальные уравнения высших порядков",
            'description': "Решить дифференциальные уравнения:\n\n1. y''' - 3y'' + 3y' - y = 0\n2. y'' + 4y' + 4y = e^(-2x)\n3. y'' - 2y' + y = x^2\n\nНайти общее и частное решения.",
            'due_date': timezone.now() + timedelta(days=10),
            'penalty_info': "За опоздание снимается 10% от максимального балла",
            'max_points': 120
        },
        {
            'subject': subjects[1],  # Физика
            'teacher': teachers[1],
            'title': "Термодинамика и молекулярная физика",
            'description': "Решить задачи по термодинамике:\n\n1. Идеальный газ расширяется изотермически. Найти работу газа.\n2. Цикл Карно. Найти КПД цикла.\n3. Энтропия и второй закон термодинамики.\n\nПоказать все расчеты.",
            'due_date': timezone.now() + timedelta(days=8),
            'penalty_info': "За опоздание снимается 15% от максимального балла",
            'max_points': 100
        },
        {
            'subject': subjects[2],  # Программирование
            'teacher': teachers[2],
            'title': "Алгоритмы и структуры данных",
            'description': "Реализовать следующие алгоритмы на Python:\n\n1. Сортировка пузырьком и быстрая сортировка\n2. Бинарное дерево поиска\n3. Хеш-таблица с разрешением коллизий\n4. Алгоритм Дейкстры для поиска кратчайшего пути\n\nКод должен быть хорошо документирован.",
            'due_date': timezone.now() + timedelta(days=15),
            'penalty_info': "За каждый день опоздания снимается 5% от максимального балла",
            'max_points': 200
        },
        {
            'subject': subjects[3],  # Базы данных
            'teacher': teachers[0],
            'title': "SQL запросы и оптимизация",
            'description': "Выполнить следующие задачи:\n\n1. Сложные JOIN запросы\n2. Подзапросы и оконные функции\n3. Индексы и их влияние на производительность\n4. Транзакции и блокировки\n\nПредоставить примеры запросов и объяснения.",
            'due_date': timezone.now() + timedelta(days=12),
            'penalty_info': "За опоздание снимается 8% от максимального балла",
            'max_points': 150
        },
        {
            'subject': subjects[4],  # Веб-разработка
            'teacher': teachers[2],
            'title': "JavaScript и AJAX",
            'description': "Создать интерактивное веб-приложение:\n\n1. Асинхронные запросы с AJAX\n2. Обработка JSON данных\n3. Динамическое обновление DOM\n4. Обработка ошибок и валидация\n\nИспользовать современный JavaScript (ES6+).",
            'due_date': timezone.now() + timedelta(days=14),
            'penalty_info': "За опоздание снимается 7% от максимального балла",
            'max_points': 180
        },
        {
            'subject': subjects[0],  # Математика
            'teacher': teachers[0],
            'title': "Комплексные числа и функции",
            'description': "Работа с комплексными числами:\n\n1. Арифметические операции с комплексными числами\n2. Тригонометрическая форма комплексного числа\n3. Формула Эйлера\n4. Решение уравнений в комплексных числах\n\nПоказать все вычисления.",
            'due_date': timezone.now() + timedelta(days=6),
            'penalty_info': "За опоздание снимается 12% от максимального балла",
            'max_points': 90
        },
        {
            'subject': subjects[1],  # Физика
            'teacher': teachers[1],
            'title': "Электромагнетизм",
            'description': "Задачи по электромагнетизму:\n\n1. Закон Кулона и напряженность электрического поля\n2. Потенциал и работа в электрическом поле\n3. Магнитное поле и сила Лоренца\n4. Электромагнитная индукция\n\nРешить с подробными объяснениями.",
            'due_date': timezone.now() + timedelta(days=9),
            'penalty_info': "За опоздание снимается 10% от максимального балла",
            'max_points': 110
        },
        {
            'subject': subjects[2],  # Программирование
            'teacher': teachers[2],
            'title': "Объектно-ориентированное программирование",
            'description': "Создать систему классов:\n\n1. Наследование и полиморфизм\n2. Инкапсуляция и абстракция\n3. Интерфейсы и абстрактные классы\n4. Паттерны проектирования (Singleton, Factory)\n\nРеализовать на Python с примерами использования.",
            'due_date': timezone.now() + timedelta(days=11),
            'penalty_info': "За опоздание снимается 6% от максимального балла",
            'max_points': 160
        },
        {
            'subject': subjects[3],  # Базы данных
            'teacher': teachers[0],
            'title': "NoSQL базы данных",
            'description': "Изучение NoSQL технологий:\n\n1. MongoDB - документо-ориентированная БД\n2. Redis - база данных ключ-значение\n3. Cassandra - колоночная БД\n4. Сравнение с реляционными БД\n\nСоздать примеры использования каждой технологии.",
            'due_date': timezone.now() + timedelta(days=13),
            'penalty_info': "За опоздание снимается 9% от максимального балла",
            'max_points': 140
        },
        {
            'subject': subjects[4],  # Веб-разработка
            'teacher': teachers[2],
            'title': "React и современный фронтенд",
            'description': "Создать SPA приложение на React:\n\n1. Компоненты и состояние\n2. Хуки (useState, useEffect)\n3. Маршрутизация с React Router\n4. Управление состоянием (Redux/Context)\n\nПриложение должно быть интерактивным и отзывчивым.",
            'due_date': timezone.now() + timedelta(days=16),
            'penalty_info': "За опоздание снимается 5% от максимального балла",
            'max_points': 220
        },
        {
            'subject': subjects[0],  # Математика
            'teacher': teachers[0],
            'title': "Теория вероятностей",
            'description': "Задачи по теории вероятностей:\n\n1. Условная вероятность и формула Байеса\n2. Дискретные и непрерывные случайные величины\n3. Математическое ожидание и дисперсия\n4. Центральная предельная теорема\n\nРешить с использованием статистических методов.",
            'due_date': timezone.now() + timedelta(days=7),
            'penalty_info': "За опоздание снимается 11% от максимального балла",
            'max_points': 130
        },
        {
            'subject': subjects[1],  # Физика
            'teacher': teachers[1],
            'title': "Квантовая механика",
            'description': "Основы квантовой механики:\n\n1. Волновая функция и уравнение Шредингера\n2. Принцип неопределенности Гейзенберга\n3. Квантование энергии\n4. Спин и магнитный момент\n\nОбъяснить физический смысл явлений.",
            'due_date': timezone.now() + timedelta(days=10),
            'penalty_info': "За опоздание снимается 13% от максимального балла",
            'max_points': 170
        },
        {
            'subject': subjects[2],  # Программирование
            'teacher': teachers[2],
            'title': "Машинное обучение с Python",
            'description': "Проект по машинному обучению:\n\n1. Предобработка данных (pandas, numpy)\n2. Обучение моделей (scikit-learn)\n3. Валидация и метрики качества\n4. Визуализация результатов (matplotlib, seaborn)\n\nСоздать модель для решения реальной задачи.",
            'due_date': timezone.now() + timedelta(days=18),
            'penalty_info': "За опоздание снимается 4% от максимального балла",
            'max_points': 250
        },
        {
            'subject': subjects[3],  # Базы данных
            'teacher': teachers[0],
            'title': "Распределенные системы",
            'description': "Архитектура распределенных систем:\n\n1. CAP теорема и консистентность\n2. Репликация и шардирование\n3. Микросервисы и контейнеризация\n4. Мониторинг и логирование\n\nСпроектировать архитектуру для высоконагруженной системы.",
            'due_date': timezone.now() + timedelta(days=20),
            'penalty_info': "За опоздание снимается 3% от максимального балла",
            'max_points': 300
        },
        {
            'subject': subjects[4],  # Веб-разработка
            'teacher': teachers[2],
            'title': "DevOps и CI/CD",
            'description': "Автоматизация разработки:\n\n1. Контейнеризация с Docker\n2. Оркестрация с Kubernetes\n3. CI/CD пайплайны (GitHub Actions, GitLab CI)\n4. Мониторинг и логирование (Prometheus, Grafana)\n\nНастроить полный цикл разработки и деплоя.",
            'due_date': timezone.now() + timedelta(days=22),
            'penalty_info': "За опоздание снимается 2% от максимального балла",
            'max_points': 280
        }
    ]
    
    created_assignments = []
    for assignment_data in additional_assignments:
        assignment = Assignment.objects.create(**assignment_data)
        created_assignments.append(assignment)
        print(f"Создано задание: {assignment.title}")
    
    print(f"\nВсего создано дополнительных заданий: {len(created_assignments)}")
    print(f"Общее количество заданий в системе: {Assignment.objects.count()}")
    
    return created_assignments

if __name__ == "__main__":
    add_more_assignments()
