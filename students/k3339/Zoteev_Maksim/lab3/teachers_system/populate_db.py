#!/usr/bin/env python
"""
Скрипт для заполнения базы данных тестовыми данными
"""

import os
import sys
import django
from datetime import date
import random

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_project.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from school.models import (
    Subject, Classroom, Teacher, TeacherSubject, SchoolClass,
    Student, Quarter, TeachingAssignment, Schedule, Grade
)


def create_subjects():
    """Создание предметов"""
    subjects_data = [
        ('Математика', 'basic'),
        ('Русский язык', 'basic'),
        ('Литература', 'basic'),
        ('Английский язык', 'basic'),
        ('История', 'basic'),
        ('Обществознание', 'basic'),
        ('География', 'basic'),
        ('Биология', 'basic'),
        ('Физика', 'profile'),
        ('Химия', 'profile'),
        ('Информатика', 'profile'),
        ('Физкультура', 'basic'),
        ('ОБЖ', 'basic'),
        ('Музыка', 'basic'),
        ('ИЗО', 'basic'),
    ]
    
    subjects = []
    for name, subject_type in subjects_data:
        subject, created = Subject.objects.get_or_create(
            name=name,
            defaults={'subject_type': subject_type}
        )
        subjects.append(subject)
        if created:
            print(f'  Создан предмет: {name}')
    
    return subjects


def create_classrooms():
    """Создание кабинетов"""
    classrooms_data = [
        ('101', 'basic', 'Кабинет начальных классов'),
        ('102', 'basic', 'Кабинет начальных классов'),
        ('201', 'basic', 'Кабинет русского языка'),
        ('202', 'basic', 'Кабинет литературы'),
        ('203', 'basic', 'Кабинет истории'),
        ('204', 'basic', 'Кабинет географии'),
        ('301', 'profile', 'Кабинет физики'),
        ('302', 'profile', 'Кабинет химии'),
        ('303', 'profile', 'Компьютерный класс'),
        ('304', 'profile', 'Кабинет математики'),
        ('305', 'basic', 'Кабинет английского языка'),
        ('401', 'basic', 'Спортивный зал'),
        ('402', 'basic', 'Актовый зал'),
    ]
    
    classrooms = []
    for number, classroom_type, description in classrooms_data:
        classroom, created = Classroom.objects.get_or_create(
            number=number,
            defaults={'classroom_type': classroom_type, 'description': description}
        )
        classrooms.append(classroom)
        if created:
            print(f'  Создан кабинет: {number}')
    
    return classrooms


def create_teachers(classrooms, subjects):
    """Создание учителей"""
    teachers_data = [
        ('Иванов', 'Иван', 'Иванович', '304', ['Математика', 'Информатика']),
        ('Петрова', 'Мария', 'Сергеевна', '201', ['Русский язык', 'Литература']),
        ('Сидоров', 'Алексей', 'Петрович', '301', ['Физика']),
        ('Козлова', 'Елена', 'Андреевна', '302', ['Химия', 'Биология']),
        ('Смирнов', 'Дмитрий', 'Владимирович', '303', ['Информатика']),
        ('Новикова', 'Ольга', 'Николаевна', '305', ['Английский язык']),
        ('Федоров', 'Сергей', 'Михайлович', '203', ['История', 'Обществознание']),
        ('Морозова', 'Анна', 'Дмитриевна', '204', ['География']),
        ('Волков', 'Павел', 'Александрович', '401', ['Физкультура', 'ОБЖ']),
        ('Егорова', 'Татьяна', 'Владимировна', None, ['Музыка', 'ИЗО']),
        ('Кузнецов', 'Андрей', 'Сергеевич', None, ['Математика']),
        ('Соколова', 'Наталья', 'Петровна', None, ['Русский язык']),
    ]
    
    classroom_map = {c.number: c for c in classrooms}
    subject_map = {s.name: s for s in subjects}
    
    teachers = []
    for last_name, first_name, patronymic, classroom_num, subject_names in teachers_data:
        classroom = classroom_map.get(classroom_num)
        
        teacher, created = Teacher.objects.get_or_create(
            last_name=last_name,
            first_name=first_name,
            defaults={
                'patronymic': patronymic,
                'classroom': classroom
            }
        )
        teachers.append(teacher)
        
        if created:
            print(f'  Создан учитель: {last_name} {first_name}')
            
            # Добавляем предметы учителю
            for subject_name in subject_names:
                subject = subject_map.get(subject_name)
                if subject:
                    TeacherSubject.objects.get_or_create(
                        teacher=teacher,
                        subject=subject
                    )
    
    return teachers


def create_classes(teachers):
    """Создание классов"""
    classes_data = [
        (5, 'А'), (5, 'Б'),
        (6, 'А'), (6, 'Б'),
        (7, 'А'), (7, 'Б'),
        (8, 'А'), (8, 'Б'),
        (9, 'А'), (9, 'Б'),
        (10, 'А'), (10, 'Б'),
        (11, 'А'), (11, 'Б'),
    ]
    
    classes = []
    available_teachers = list(teachers)  # Копия списка учителей
    
    for number, letter in classes_data:
        # Назначаем классного руководителя из доступных учителей
        class_teacher = None
        if available_teachers:
            class_teacher = available_teachers.pop(0)
        
        school_class, created = SchoolClass.objects.get_or_create(
            number=number,
            letter=letter,
            defaults={'class_teacher': class_teacher}
        )
        classes.append(school_class)
        
        if created:
            print(f'  Создан класс: {number}{letter}')
    
    return classes


def create_students(classes):
    """Создание учеников"""
    first_names_m = ['Александр', 'Дмитрий', 'Максим', 'Артём', 'Иван', 
                     'Кирилл', 'Никита', 'Михаил', 'Егор', 'Даниил']
    first_names_f = ['Анастасия', 'Мария', 'Дарья', 'Анна', 'Елизавета',
                     'Виктория', 'Полина', 'Алиса', 'София', 'Екатерина']
    last_names = ['Иванов', 'Петров', 'Сидоров', 'Козлов', 'Смирнов',
                  'Новиков', 'Федоров', 'Морозов', 'Волков', 'Егоров',
                  'Кузнецов', 'Соколов', 'Попов', 'Лебедев', 'Павлов']
    
    students = []
    
    for school_class in classes:
        # В каждом классе ~20-25 учеников
        num_students = random.randint(20, 25)
        
        for i in range(num_students):
            gender = random.choice(['M', 'F'])
            
            if gender == 'M':
                first_name = random.choice(first_names_m)
                last_name = random.choice(last_names)
            else:
                first_name = random.choice(first_names_f)
                last_name = random.choice(last_names) + 'а'
            
            # Добавляем номер для уникальности
            unique_suffix = f'{school_class.id}{i}'
            
            student, created = Student.objects.get_or_create(
                first_name=first_name,
                last_name=f'{last_name}_{unique_suffix}',
                defaults={
                    'gender': gender,
                    'school_class': school_class
                }
            )
            students.append(student)
    
    print(f'  Создано учеников: {len(students)}')
    return students


def create_quarters():
    """Создание четвертей"""
    quarters_data = [
        (1, '2024-2025', date(2024, 9, 1), date(2024, 10, 27), False),
        (2, '2024-2025', date(2024, 11, 5), date(2024, 12, 29), True),
        (3, '2024-2025', date(2025, 1, 9), date(2025, 3, 23), False),
        (4, '2024-2025', date(2025, 4, 1), date(2025, 5, 25), False),
    ]
    
    quarters = []
    for number, academic_year, start_date, end_date, is_current in quarters_data:
        quarter, created = Quarter.objects.get_or_create(
            number=number,
            academic_year=academic_year,
            defaults={
                'start_date': start_date,
                'end_date': end_date,
                'is_current': is_current
            }
        )
        quarters.append(quarter)
        if created:
            print(f'  Создана четверть: {quarter}')
    
    return quarters


def create_teaching_assignments(teachers, subjects, classes, quarters):
    """Создание назначений преподавания"""
    subject_map = {s.name: s for s in subjects}
    current_quarter = [q for q in quarters if q.is_current][0]
    
    # Распределение предметов по учителям для каждого класса
    assignments = []
    
    for school_class in classes:
        # Базовые предметы для всех классов
        base_subjects = ['Математика', 'Русский язык', 'Литература', 'Английский язык',
                        'История', 'Физкультура']
        
        # Дополнительные предметы для старших классов
        if school_class.number >= 7:
            base_subjects.extend(['Физика', 'Информатика', 'География', 'Биология'])
        
        if school_class.number >= 8:
            base_subjects.extend(['Химия', 'Обществознание'])
        
        for subject_name in base_subjects:
            subject = subject_map.get(subject_name)
            if not subject:
                continue
            
            # Находим учителя, который преподает этот предмет
            teacher_subjects = TeacherSubject.objects.filter(subject=subject)
            if not teacher_subjects.exists():
                continue
            
            teacher = random.choice(list(teacher_subjects)).teacher
            
            assignment, created = TeachingAssignment.objects.get_or_create(
                teacher=teacher,
                subject=subject,
                school_class=school_class,
                quarter=current_quarter
            )
            assignments.append(assignment)
    
    print(f'  Создано назначений: {len(assignments)}')
    return assignments


def create_schedule(assignments, classrooms):
    """Создание расписания"""
    classroom_map = {c.number: c for c in classrooms}
    
    # Расписание звонков (номера уроков)
    lessons_per_day = 6
    
    schedule_entries = []
    
    # Группируем назначения по классам
    class_assignments = {}
    for assignment in assignments:
        class_id = assignment.school_class_id
        if class_id not in class_assignments:
            class_assignments[class_id] = []
        class_assignments[class_id].append(assignment)
    
    for class_id, class_assignments_list in class_assignments.items():
        # Для каждого класса создаем расписание на неделю
        assignment_index = 0
        
        for day in range(1, 7):  # 6 дней в неделю
            lessons_today = lessons_per_day if day < 6 else 4  # В субботу меньше уроков
            
            for lesson in range(1, lessons_today + 1):
                if assignment_index >= len(class_assignments_list):
                    assignment_index = 0
                
                assignment = class_assignments_list[assignment_index]
                
                # Выбираем кабинет (предпочтительно закрепленный за учителем)
                classroom = assignment.teacher.classroom
                if not classroom:
                    classroom = random.choice(classrooms)
                
                schedule, created = Schedule.objects.get_or_create(
                    teaching_assignment=assignment,
                    day_of_week=day,
                    lesson_number=lesson,
                    defaults={'classroom': classroom}
                )
                schedule_entries.append(schedule)
                assignment_index += 1
    
    print(f'  Создано записей расписания: {len(schedule_entries)}')
    return schedule_entries


def create_grades(students, subjects, quarters):
    """Создание оценок"""
    current_quarter = [q for q in quarters if q.is_current][0]
    
    grades = []
    
    for student in students:
        # Получаем предметы, которые преподаются в классе ученика
        class_subjects = TeachingAssignment.objects.filter(
            school_class=student.school_class,
            quarter=current_quarter
        ).values_list('subject', flat=True).distinct()
        
        for subject_id in class_subjects:
            subject = Subject.objects.get(id=subject_id)
            
            # Генерируем случайную оценку (с перевесом в сторону хороших оценок)
            grade_value = random.choices([2, 3, 4, 5], weights=[5, 15, 40, 40])[0]
            
            grade, created = Grade.objects.get_or_create(
                student=student,
                subject=subject,
                quarter=current_quarter,
                defaults={'value': grade_value}
            )
            grades.append(grade)
    
    print(f'  Создано оценок: {len(grades)}')
    return grades


def create_superuser():
    """Создание суперпользователя"""
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@school.local',
            password='admin123'
        )
        print('  Создан суперпользователь: admin / admin123')
    else:
        print('  Суперпользователь уже существует')


def main():
    print('=' * 50)
    print('Заполнение базы данных тестовыми данными')
    print('=' * 50)
    
    print('\n1. Создание суперпользователя...')
    create_superuser()
    
    print('\n2. Создание предметов...')
    subjects = create_subjects()
    
    print('\n3. Создание кабинетов...')
    classrooms = create_classrooms()
    
    print('\n4. Создание учителей...')
    teachers = create_teachers(classrooms, subjects)
    
    print('\n5. Создание классов...')
    classes = create_classes(teachers)
    
    print('\n6. Создание учеников...')
    students = create_students(classes)
    
    print('\n7. Создание четвертей...')
    quarters = create_quarters()
    
    print('\n8. Создание назначений преподавания...')
    assignments = create_teaching_assignments(teachers, subjects, classes, quarters)
    
    print('\n9. Создание расписания...')
    create_schedule(assignments, classrooms)
    
    print('\n10. Создание оценок...')
    create_grades(students, subjects, quarters)
    
    print('\n' + '=' * 50)
    print('База данных успешно заполнена!')
    print('=' * 50)
    print('\nДля входа в админ-панель используйте:')
    print('  Логин: admin')
    print('  Пароль: admin123')
    print('\nЗапустите сервер командой:')
    print('  python manage.py runserver')


if __name__ == '__main__':
    main()

