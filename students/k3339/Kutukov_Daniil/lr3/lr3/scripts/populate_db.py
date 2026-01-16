import os
import sys
import django
from datetime import datetime, timedelta
import random

# Настройка окружения Django
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "college_system.settings")
django.setup()

from education.models import (
    Classroom,
    Subject,
    Teacher,
    Group,
    Student,
    Grade,
    Schedule,
)


def clear_db():
    """Очистить базу данных"""
    print("Очистка базы данных...")
    Schedule.objects.all().delete()
    Grade.objects.all().delete()
    Student.objects.all().delete()
    Group.objects.all().delete()
    Teacher.objects.all().delete()
    Subject.objects.all().delete()
    Classroom.objects.all().delete()
    print("База данных очищена")


def create_classrooms():
    """Создать кабинеты"""
    print("Создание кабинетов...")
    classrooms = []

    # Лекционные аудитории
    for i in range(1, 6):
        classrooms.append(
            Classroom.objects.create(number=f"Л-{i}", capacity=100 + i * 10)
        )

    # Практические кабинеты
    for i in range(1, 11):
        classrooms.append(
            Classroom.objects.create(number=f"{100 + i}", capacity=20 + i * 2)
        )

    # Компьютерные классы
    for i in range(1, 4):
        classrooms.append(Classroom.objects.create(number=f"К-{i}", capacity=15))

    print(f"Создано {len(classrooms)} кабинетов")
    return classrooms


def create_subjects():
    """Создать дисциплины"""
    print("Создание дисциплин...")
    subjects_data = [
        ("Математический анализ", 144),
        ("Линейная алгебра", 108),
        ("Дискретная математика", 108),
        ("Программирование", 180),
        ("Базы данных", 144),
        ("Алгоритмы и структуры данных", 144),
        ("Операционные системы", 108),
        ("Компьютерные сети", 108),
        ("Объектно-ориентированное программирование", 144),
        ("Веб-разработка", 108),
        ("Физика", 144),
        ("Английский язык", 216),
        ("Философия", 72),
        ("История", 72),
    ]

    subjects = []
    for name, hours in subjects_data:
        subjects.append(Subject.objects.create(name=name, hours_per_semester=hours))

    print(f"Создано {len(subjects)} дисциплин")
    return subjects


def create_teachers(classrooms, subjects):
    """Создать преподавателей"""
    print("Создание преподавателей...")
    teachers_data = [
        ("Иванов", "Иван", "Иванович", [0, 1, 2]),
        ("Петрова", "Мария", "Сергеевна", [3, 4, 5]),
        ("Сидоров", "Петр", "Александрович", [6, 7]),
        ("Кузнецова", "Анна", "Владимировна", [8, 9]),
        ("Смирнов", "Алексей", "Дмитриевич", [10]),
        ("Попова", "Елена", "Игоревна", [11]),
        ("Васильев", "Дмитрий", "Николаевич", [12, 13]),
        ("Федорова", "Ольга", "Андреевна", [0, 3]),
        ("Морозов", "Сергей", "Викторович", [4, 8]),
        ("Новикова", "Татьяна", "Павловна", [1, 5]),
    ]

    teachers = []
    for idx, (last, first, middle, subject_indices) in enumerate(teachers_data):
        teacher = Teacher.objects.create(
            last_name=last,
            first_name=first,
            middle_name=middle,
            classroom=classrooms[idx % len(classrooms)],
        )
        teacher.subjects.set([subjects[i] for i in subject_indices])
        teachers.append(teacher)

    print(f"Создано {len(teachers)} преподавателей")
    return teachers


def create_groups():
    """Создать группы"""
    print("Создание групп...")
    groups = []

    specialties = [
        "Прикладная информатика",
        "Программная инженерия",
        "Информационные системы",
    ]

    # Группы по курсам
    for course in range(1, 5):
        for group_num in range(1, 4):
            groups.append(
                Group.objects.create(
                    name=f"ПИ-{course}{group_num}",
                    course=course,
                    specialty=specialties[(course + group_num) % len(specialties)],
                )
            )

    print(f"Создано {len(groups)} групп")
    return groups


def create_students(groups):
    """Создать студентов"""
    print("Создание студентов...")

    first_names_male = [
        "Александр",
        "Дмитрий",
        "Максим",
        "Артём",
        "Иван",
        "Михаил",
        "Даниил",
        "Егор",
    ]
    first_names_female = [
        "Анастасия",
        "Мария",
        "Дарья",
        "Анна",
        "Полина",
        "Екатерина",
        "Виктория",
        "Алина",
    ]
    last_names_male = [
        "Иванов",
        "Петров",
        "Сидоров",
        "Козлов",
        "Волков",
        "Зайцев",
        "Соколов",
        "Новиков",
    ]
    last_names_female = [
        "Иванова",
        "Петрова",
        "Сидорова",
        "Козлова",
        "Волкова",
        "Зайцева",
        "Соколова",
        "Новикова",
    ]
    middle_names_male = [
        "Александрович",
        "Дмитриевич",
        "Максимович",
        "Иванович",
        "Михайлович",
        "Сергеевич",
    ]
    middle_names_female = [
        "Александровна",
        "Дмитриевна",
        "Максимовна",
        "Ивановна",
        "Михайловна",
        "Сергеевна",
    ]

    students = []

    for group in groups:
        # От 20 до 30 студентов в группе
        students_in_group = random.randint(20, 30)

        # Дата зачисления зависит от курса
        enrollment_year = datetime.now().year - (group.course - 1)
        enrollment_date = datetime(enrollment_year, 9, 1).date()

        for _ in range(students_in_group):
            is_male = random.choice([True, False])

            if is_male:
                first_name = random.choice(first_names_male)
                last_name = random.choice(last_names_male)
                middle_name = random.choice(middle_names_male)
            else:
                first_name = random.choice(first_names_female)
                last_name = random.choice(last_names_female)
                middle_name = random.choice(middle_names_female)

            students.append(
                Student.objects.create(
                    last_name=last_name,
                    first_name=first_name,
                    middle_name=middle_name,
                    enrollment_date=enrollment_date,
                    group=group,
                )
            )

    print(f"Создано {len(students)} студентов")
    return students


def create_schedule(groups, subjects, teachers, classrooms):
    """Создать расписание"""
    print("Создание расписания...")
    schedules = []

    # Стандартное время начала уроков
    lesson_times = {
        1: ("09:00", "10:30"),
        2: ("10:45", "12:15"),
        3: ("12:30", "14:00"),
        4: ("14:15", "15:45"),
        5: ("16:00", "17:30"),
        6: ("17:45", "19:15"),
    }

    # Отслеживание занятости
    group_schedule = set()  # (group_id, day, lesson)
    teacher_schedule = set()  # (teacher_id, day, lesson)
    classroom_schedule = set()  # (classroom_id, day, lesson)

    # Для каждой группы создаем расписание
    for group in groups:
        # Выбираем предметы для курса (примерно 5-7 предметов)
        group_subjects = random.sample(subjects, random.randint(5, 7))

        for subject in group_subjects:
            # Находим преподавателей, ведущих этот предмет
            available_teachers = [t for t in teachers if subject in t.subjects.all()]

            if not available_teachers:
                continue

            # Количество пар в неделю (1-2)
            lessons_per_week = random.randint(1, 2)

            attempts = 0
            lessons_created = 0

            while lessons_created < lessons_per_week and attempts < 100:
                day = random.randint(1, 6)
                lesson = random.randint(1, 6)

                # Проверяем, свободна ли группа
                if (group.id, day, lesson) in group_schedule:
                    attempts += 1
                    continue

                # Ищем свободного преподавателя
                teacher_found = False
                random.shuffle(available_teachers)

                for teacher in available_teachers:
                    if (teacher.id, day, lesson) not in teacher_schedule:
                        # Преподаватель свободен, ищем свободный кабинет
                        random.shuffle(classrooms)

                        for classroom in classrooms:
                            if (classroom.id, day, lesson) not in classroom_schedule:
                                # Все свободно, создаем запись
                                start_time, end_time = lesson_times[lesson]
                                schedules.append(
                                    Schedule.objects.create(
                                        group=group,
                                        subject=subject,
                                        teacher=teacher,
                                        classroom=classroom,
                                        day_of_week=day,
                                        lesson_number=lesson,
                                        start_time=start_time,
                                        end_time=end_time,
                                    )
                                )

                                # Отмечаем как занятое
                                group_schedule.add((group.id, day, lesson))
                                teacher_schedule.add((teacher.id, day, lesson))
                                classroom_schedule.add((classroom.id, day, lesson))

                                lessons_created += 1
                                teacher_found = True
                                break

                        if teacher_found:
                            break

                attempts += 1

    print(f"Создано {len(schedules)} записей расписания")
    return schedules


def create_grades(students, subjects):
    """Создать оценки"""
    print("Создание оценок...")
    grades = []

    grade_values = [2, 3, 3, 3, 4, 4, 4, 4, 5, 5]  # Взвешенное распределение оценок

    for student in students:
        # Получаем предметы для курса студента
        course_subjects = random.sample(
            subjects, random.randint(5, min(8, len(subjects)))
        )

        for subject in course_subjects:
            # Семестры, в которых изучается предмет (только один семестр для уникальности)
            semester = random.randint(1, min(student.group.course * 2, 8))

            # Дата в пределах семестра
            base_date = datetime.now() - timedelta(days=random.randint(0, 180))

            # Создаем только одну запись на комбинацию студент-предмет-семестр
            grades.append(
                Grade.objects.create(
                    student=student,
                    subject=subject,
                    grade=random.choice(grade_values),
                    semester=semester,
                    date=base_date.date(),
                )
            )

    print(f"Создано {len(grades)} оценок")
    return grades


def populate():
    """Заполнить базу данных тестовыми данными"""
    print("=" * 50)
    print("Начало заполнения базы данных")
    print("=" * 50)

    clear_db()

    classrooms = create_classrooms()
    subjects = create_subjects()
    teachers = create_teachers(classrooms, subjects)
    groups = create_groups()
    students = create_students(groups)
    schedules = create_schedule(groups, subjects, teachers, classrooms)
    grades = create_grades(students, subjects)

    print("=" * 50)
    print("База данных успешно заполнена!")
    print("=" * 50)
    print(f"Кабинетов: {len(classrooms)}")
    print(f"Дисциплин: {len(subjects)}")
    print(f"Преподавателей: {len(teachers)}")
    print(f"Групп: {len(groups)}")
    print(f"Студентов: {len(students)}")
    print(f"Записей расписания: {len(schedules)}")
    print(f"Оценок: {len(grades)}")
    print("=" * 50)


if __name__ == "__main__":
    populate()
