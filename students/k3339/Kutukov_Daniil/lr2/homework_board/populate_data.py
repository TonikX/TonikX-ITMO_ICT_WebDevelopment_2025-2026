#!/usr/bin/env python
import os
import sys
import django
from datetime import date, datetime, timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homework_board.settings')
django.setup()

from assignments.models import User, Subject, Assignment, Submission, Grade

def create_test_data():
    """Создание тестовых данных"""
    
    subjects = [
        Subject.objects.create(name="Математика", description="Высшая математика и математический анализ"),
        Subject.objects.create(name="Физика", description="Общая физика и механика"),
        Subject.objects.create(name="Программирование", description="Основы программирования на Python"),
        Subject.objects.create(name="Базы данных", description="Проектирование и управление базами данных"),
        Subject.objects.create(name="Веб-разработка", description="Создание веб-приложений"),
    ]
            
    teachers = [
        User.objects.create_user(
            username='teacher1',
            email='teacher1@university.edu',
            password='password123',
            first_name='Анна',
            last_name='Петрова',
            role=User.TEACHER,
            phone='+7-900-123-4567',
            birth_date=date(1980, 5, 15)
        ),
        User.objects.create_user(
            username='teacher2',
            email='teacher2@university.edu',
            password='password123',
            first_name='Михаил',
            last_name='Сидоров',
            role=User.TEACHER,
            phone='+7-900-234-5678',
            birth_date=date(1975, 8, 22)
        ),
        User.objects.create_user(
            username='teacher3',
            email='teacher3@university.edu',
            password='password123',
            first_name='Елена',
            last_name='Козлова',
            role=User.TEACHER,
            phone='+7-900-345-6789',
            birth_date=date(1982, 3, 10)
        ),
    ]
    
    students = [
        User.objects.create_user(
            username='student1',
            email='student1@university.edu',
            password='password123',
            first_name='Иван',
            last_name='Иванов',
            role=User.STUDENT,
            student_id='2023001',
            phone='+7-900-111-1111',
            birth_date=date(2000, 1, 15)
        ),
        User.objects.create_user(
            username='student2',
            email='student2@university.edu',
            password='password123',
            first_name='Мария',
            last_name='Петрова',
            role=User.STUDENT,
            student_id='2023002',
            phone='+7-900-222-2222',
            birth_date=date(2000, 3, 20)
        ),
        User.objects.create_user(
            username='student3',
            email='student3@university.edu',
            password='password123',
            first_name='Алексей',
            last_name='Смирнов',
            role=User.STUDENT,
            student_id='2023003',
            phone='+7-900-333-3333',
            birth_date=date(2000, 7, 5)
        ),
        User.objects.create_user(
            username='student4',
            email='student4@university.edu',
            password='password123',
            first_name='Анна',
            last_name='Волкова',
            role=User.STUDENT,
            student_id='2023004',
            phone='+7-900-444-4444',
            birth_date=date(2000, 11, 12)
        ),
        User.objects.create_user(
            username='student5',
            email='student5@university.edu',
            password='password123',
            first_name='Дмитрий',
            last_name='Козлов',
            role=User.STUDENT,
            student_id='2023005',
            phone='+7-900-555-5555',
            birth_date=date(2000, 4, 8)
        ),
    ]
    
    assignments = [
        Assignment.objects.create(
            subject=subjects[0],
            teacher=teachers[0],
            title="Интегралы и дифференциальные уравнения",
            description="Решить следующие интегралы и дифференциальные уравнения:\n\n1. ∫(x² + 3x + 2)dx\n2. ∫sin(x)cos(x)dx\n3. y' + 2y = e^(-x)\n4. y'' - 4y' + 4y = 0\n\nПоказать все этапы решения.",
            due_date=timezone.now() + timedelta(days=7),
            penalty_info="За каждый день опоздания снимается 10% от максимального балла",
            max_points=100
        ),
        Assignment.objects.create(
            subject=subjects[1],
            teacher=teachers[1],
            title="Законы Ньютона и кинематика",
            description="Решить задачи по кинематике:\n\n1. Тело движется по закону x(t) = 2t³ - 3t² + 5. Найти скорость и ускорение в момент времени t=2с.\n2. Шарик брошен под углом 30° к горизонту со скоростью 20 м/с. Найти максимальную высоту и дальность полета.\n3. На наклонной плоскости с углом 30° лежит брусок массой 2 кг. Найти ускорение бруска, если коэффициент трения 0.3.",
            due_date=timezone.now() + timedelta(days=5),
            penalty_info="За опоздание снимается 15% от максимального балла",
            max_points=80
        ),
        Assignment.objects.create(
            subject=subjects[2],
            teacher=teachers[2],
            title="Создание веб-приложения на Django",
            description="Создать веб-приложение для управления задачами со следующими функциями:\n\n1. Модели: User, Task, Category\n2. Админ-панель для управления\n3. Формы для создания и редактирования задач\n4. Поиск и фильтрация задач\n5. Пагинация списка задач\n\nКод должен быть хорошо документирован и покрыт тестами.",
            due_date=timezone.now() + timedelta(days=14),
            penalty_info="За каждый день опоздания снимается 5% от максимального балла",
            max_points=150
        ),
        Assignment.objects.create(
            subject=subjects[3],
            teacher=teachers[0],
            title="Проектирование схемы базы данных",
            description="Спроектировать схему базы данных для интернет-магазина:\n\n1. ER-диаграмма\n2. Нормализация до 3NF\n3. SQL-скрипты создания таблиц\n4. Индексы и ограничения\n5. Примеры запросов (SELECT, INSERT, UPDATE, DELETE)",
            due_date=timezone.now() + timedelta(days=10),
            penalty_info="За опоздание снимается 10% от максимального балла",
            max_points=120
        ),
        Assignment.objects.create(
            subject=subjects[4],
            teacher=teachers[2],
            title="Адаптивный дизайн с Bootstrap",
            description="Создать адаптивную веб-страницу с использованием Bootstrap 5:\n\n1. Навигационное меню\n2. Карточки с контентом\n3. Формы с валидацией\n4. Модальные окна\n5. Адаптивность для мобильных устройств\n\nИспользовать современные CSS-техники и JavaScript.",
            due_date=timezone.now() + timedelta(days=12),
            penalty_info="За опоздание снимается 8% от максимального балла",
            max_points=100
        ),
    ]
    
    submissions = []
    
    for assignment in assignments:
        submission = Submission.objects.create(
            assignment=assignment,
            student=students[0],
            content=f"Решение задания '{assignment.title}':\n\nЗдесь должно быть подробное решение с объяснениями и выводами. Студент {students[0].get_full_name()} выполнил задание в срок."
        )
        submissions.append(submission)
    
    for assignment in assignments[:3]:
        submission = Submission.objects.create(
            assignment=assignment,
            student=students[1],
            content=f"Решение задания '{assignment.title}':\n\nДетальное решение с пошаговыми объяснениями. Студент {students[1].get_full_name()} предоставляет качественное решение."
        )
        submissions.append(submission)
    
    for i, assignment in enumerate(assignments[:2]):
        is_late = i == 1
        submission = Submission.objects.create(
            assignment=assignment,
            student=students[2],
            content=f"Решение задания '{assignment.title}':\n\n{'[СДАНО С ОПОЗДАНИЕМ] ' if is_late else ''}Решение предоставлено студентом {students[2].get_full_name()}."
        )
        if is_late:
            submission.is_late = True
            submission.save()
        submissions.append(submission)
    
    for assignment in assignments[:4]:
        submission = Submission.objects.create(
            assignment=assignment,
            student=students[3],
            content=f"Решение задания '{assignment.title}':\n\nКачественное решение с подробными комментариями от студента {students[3].get_full_name()}."
        )
        submissions.append(submission)
    
    submission = Submission.objects.create(
        assignment=assignments[0],
        student=students[4],
        content=f"Решение задания '{assignments[0].title}':\n\nКраткое решение от студента {students[4].get_full_name()}."
    )
    submissions.append(submission)
    
    grades = []
    
    for i, submission in enumerate(submissions[:5]):
        points = [95, 88, 92, 90, 87][i]
        grade = Grade.objects.create(
            submission=submission,
            points=points,
            feedback=f"Отличная работа! Оценка {points}/{submission.assignment.max_points}. {'Есть небольшие замечания по оформлению.' if points < 95 else 'Работа выполнена безупречно.'}",
            graded_by=teachers[0]   
        )
        grades.append(grade)
    
    for i, submission in enumerate(submissions[5:8]):
        points = [82, 85, 78][i]
        grade = Grade.objects.create(
            submission=submission,
            points=points,
            feedback=f"Хорошая работа. Оценка {points}/{submission.assignment.max_points}. {'Можно улучшить детализацию решения.' if points < 85 else 'Решение качественное.'}",
            graded_by=teachers[1] if i < 2 else teachers[2]
        )
        grades.append(grade)
    
    for i, submission in enumerate(submissions[8:10]):
        points = [75, 60][i]
        feedback = f"Оценка {points}/{submission.assignment.max_points}. "
        if i == 1:
            feedback += "Задание сдано с опозданием, что повлияло на оценку. "
        feedback += "Решение требует доработки."
        
        grade = Grade.objects.create(
            submission=submission,
            points=points,
            feedback=feedback,
            graded_by=teachers[0] if i == 0 else teachers[1]
        )
        grades.append(grade)
    
    for i, submission in enumerate(submissions[10:14]):
        points = [88, 92, 85, 90][i]
        grade = Grade.objects.create(
            submission=submission,
            points=points,
            feedback=f"Хорошая работа. Оценка {points}/{submission.assignment.max_points}. {'Есть потенциал для улучшения.' if points < 90 else 'Отличное выполнение.'}",
            graded_by=teachers[0] if i < 2 else (teachers[1] if i == 2 else teachers[2])
        )
        grades.append(grade)
    
    grade = Grade.objects.create(
        submission=submissions[14],
        points=70,
        feedback=f"Оценка 70/{submissions[14].assignment.max_points}. Решение базовое, требует доработки и более детального подхода.",
        graded_by=teachers[0]
    )
    grades.append(grade)
    
    print("Тестовые данные успешно созданы!")
    print(f"Создано предметов: {Subject.objects.count()}")
    print(f"Создано пользователей: {User.objects.count()}")
    print(f"Создано заданий: {Assignment.objects.count()}")
    print(f"Создано сдач: {Submission.objects.count()}")
    print(f"Создано оценок: {Grade.objects.count()}")
    
    print("\nТестовые учетные записи:")
    print("Преподаватели:")
    for teacher in teachers:
        print(f"  {teacher.username} / password123 ({teacher.get_full_name()})")
    
    print("\nСтуденты:")
    for student in students:
        print(f"  {student.username} / password123 ({student.get_full_name()})")

if __name__ == "__main__":
    create_test_data()
